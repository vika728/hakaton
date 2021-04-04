from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def get_product_url(obj, viewname, model_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


# 1.Category
# 2. Product
# 3. CartProduct
# 4. Cart
# 5. Order
# 6. Customer - покупатель
# 7. Description


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    # parent_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_category', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Именование')
    slug = models.SlugField(unique=True, default=1)
    image = models.ImageField(verbose_name='Изоражение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.PositiveIntegerField(max_length=9, verbose_name='Цена')
    brand_name = models.CharField(max_length=50, name='Бренд')
    country = models.CharField(max_length=55, name='Страна бренда')

    def __str__(self):
        return self.title



class Foundation(Product):
    STATUS_CHOICES = (('for dry', 'Для сухой кожи'), ('for mixed', 'Ддя комбинированного типа кожи'),
                      ('for oily', 'Для жирной кожи'), ('for normal', 'Для нормальной кожи'))
    skin_type = models.CharField(choices=STATUS_CHOICES, max_length=20)
    shades = models.CharField(max_length=2, name='Оттенок')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class ForEyes(Product):
    STATUS_CHOICES = (('shades', 'Тени для век'), ('eyeliner', 'Подводка'),
                      ('glitter', 'Глиттер'), ('Mascara', 'тушь'))
    products_for = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class ForBrows(Product):
    STATUS_CHOICES = (('shades', 'Тени для бровей'), ('marker', 'Фломастер'),
                      ('gel', 'Гель'), ('pencil', 'Карандаш'))
    products_for = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class ForLips(Product):
    STATUS_CHOICES = (('creamy', 'Кремовая помада'), ('gloss', 'Блеск'),
                      ('mate', 'Матовая помада'), ('pencil for lips', 'Карандаш для губ'))
    products_for = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.IntegerField(max_length=9, verbose_name='Общая Цена')

    def __str__(self):
        return f'Продукты для корзины {self.content_object.title}'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.IntegerField(max_length=9, verbose_name='Общая Цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Полльзователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=19, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'Покупатель {self.user.first_name} {self.user.last_name}'

#
# class Specification(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=255, verbose_name='Имя товара для характеристик')
#
#     def __str__(self):
#         return f'Характеристики для товаров {self.name}'

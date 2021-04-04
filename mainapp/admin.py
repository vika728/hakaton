from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField


class FoundationAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Имя категории':
            return ModelChoiceField(Category.objects.filter(slug='foundation'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class ForEyesCategoryChoiceField(forms.ModelChoiceField):
#     pass


class ForEyesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Имя категории':
            return ModelChoiceField(Category.objects.filter(slug='foreyes'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#
# class ForBrowsCategoryChoiceField(forms.ModelChoiceField):
#     pass


class ForBrowsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Имя категории':
            return ModelChoiceField(Category.objects.filter(slug='forbrows'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class ForLipsCategoryChoiceField(forms.ModelChoiceField):
#     pass


class ForLipsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Имя категории':
            return ModelChoiceField(Category.objects.filter(slug='forlips'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Foundation, FoundationAdmin)
admin.site.register(ForEyes, ForEyesAdmin)
admin.site.register(ForBrows, ForBrowsAdmin)
admin.site.register(ForLips, ForLipsAdmin)
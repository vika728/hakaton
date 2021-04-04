from django.shortcuts import render
# from django.views. import DetailView
from django.views.generic import DetailView

from .models import *


def test_view(request):
    return render(request, 'index.html', {})


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'foundation': Foundation,
        'foreyes': ForEyes,
        'forbrows': ForBrows,
        'forlips': ForLips
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

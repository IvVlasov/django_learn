from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.conf import settings

from cart.forms import CartAddProductForm
from .models import Product, Category
from typing import Any


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product.html'

    def get_queryset(self):
        product = Product.objects.filter(vendor_code=self.kwargs['pk'])
        return product

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['cart_product_form'] = CartAddProductForm()
        context['relatives_color'], context['relatives'] = \
            _get_relatives(self.kwargs, product)

        print(context['relatives'])
        context['price_before_discount'] = int(product.price * 1.1)
        return context


def _get_relatives(data: dict[str, Any], product: Product):
    relatives_color = Product.objects.filter(name__contains=product.name)
    relatives = Product.objects.filter(
        category__slug=data['category_slug']
    ).order_by('?')

    for relative in relatives_color:
        relatives = relatives.exclude(name=relative.name)

    relatives_color = relatives_color.exclude(color__contains=product.color)
    return relatives_color[:4], relatives[:4]


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop.html'

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        results = self.request.GET.get(
            'results', settings.PAGE_PRODUCTS_COUNT[0]
        )
        self.paginate_by = results
        self.order_by = self.request.GET.get('order', None)
        self.ordering = '-price' if self.order_by == 'down' else 'price'

    def get_queryset(self):
        if self.order_by:
            return Product.objects.filter(
                category__slug=self.kwargs['category']
            ).order_by(self.ordering)
        return Product.objects.filter(
            category__slug=self.kwargs['category']
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(
            slug=self.kwargs['category']
        )
        context['sort_by'] = settings.ORDER_ICONS.get(self.order_by, '')
        context['products_count'] = settings.PAGE_PRODUCTS_COUNT
        context['paginate_by'] = self.paginate_by
        return context

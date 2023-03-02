from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .services.cart import Cart
from .forms import CartAddProductForm
from shop.models import Product


def cart_page(request):
    cart = Cart(request)
    return render(request, 'cart.html', context={'cart': cart})


class AddProductView(generic.edit.FormView):
    template_name = 'cart.html'
    form_class = CartAddProductForm
    success_url = reverse_lazy('cart_page')

    def form_valid(self, form):
        self._add_to_cart(form.cleaned_data)
        return super().form_valid(form)

    def _add_to_cart(self, cleaned_data):
        product = Product.objects.get(vendor_code=self.kwargs['article'])
        cart = Cart(self.request)
        cart.add(product=product,
                 quantity=cleaned_data['quantity'])


class CartRemoveRedirectView(generic.base.RedirectView):
    pattern_name = 'cart_page'

    def get_redirect_url(self, *args, **kwargs):
        cart = Cart(self.request)
        product = Product.objects.get(vendor_code=self.kwargs['article'])
        cart.remove(product)
        return super().get_redirect_url()


class CartUpdateRedirectView(generic.base.RedirectView):
    pattern_name = 'cart_page'

    def get_redirect_url(self, *args, **kwargs):
        cart = Cart(self.request)
        product = Product.objects.get(vendor_code=self.kwargs['article'])
        cart.update_quantity(product, self.kwargs['quantity'], self.kwargs['mode'])
        return super().get_redirect_url()

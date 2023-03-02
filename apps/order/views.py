from django.views import generic
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound

from .models import Order, OrderItem
from .forms import OrderCreationForm
from .services.qiwi import QiwiPayment
from cart.services.cart import Cart


class RevokeOrderView(generic.View):
    success_url = '/order/all'

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'], customer=request.user)
        order.set_cancelled()
        QiwiPayment(request.user, order).clear_db()
        return redirect(self.success_url)


def change_order_status(request, order):
    qiwi = QiwiPayment(request.user, order)
    pay_data = qiwi.get_qiwi_payment()

    if not pay_data:
        order.set_due()
        qiwi.clear_db()
        return

    status = pay_data.get('status')
    if status['value'] == 'PAID':
        order.set_paid()
        qiwi.clear_db()

    elif status['value'] == 'EXPIRED':
        order.set_due()
        qiwi.clear_db()
    else:
        return pay_data


class OrderUserDetailView(LoginRequiredMixin, generic.detail.DetailView):
    login_url = settings.LOGIN_URL
    template_name = 'orderdetails.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        order_obj = self.get_object()

        if order_obj.status != Order.CONFIRM:
            return super().get(self, request, *args, **kwargs)

        pay_data = change_order_status(self.request, order_obj)
        if pay_data:
            self.pay_url = pay_data.get('payUrl')
            self.date_expire = pay_data.get('expirationDateTime')
        return super().get(self, request, *args, kwargs)

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs['pk'],
                                    customer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.status == Order.CONFIRM:
            context['pay_url'] = self.pay_url
            context['date_expire'] = self.date_expire
        return context


class OrdersUserListView(generic.list.ListView):
    template_name = 'user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(
            customer__id=self.request.user.id
        ).order_by('-id')


class OrderCreateView(LoginRequiredMixin, generic.edit.FormView):
    login_url = settings.LOGIN_URL
    template_name = 'order.html'
    form_class = OrderCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        self._create_order(form.cleaned_data)
        return super().form_valid(form)

    def _create_order(self, adress_data):
        current_user = self.request.user
        cart = Cart(self.request)
        adress = ', '.join(adress_data.values())

        self.order = Order.objects.create(customer=current_user,
                                          amount=cart.get_total_price(),
                                          delivery_adres=adress)
        for item in cart:
            OrderItem.objects.create(order=self.order,
                                     product=item['product'],
                                     quanity=item['quantity'],
                                     product_price=item['product'].price)
        cart.clear()

    def get_success_url(self):
        qiwi_pay = QiwiPayment(self.request.user, self.order)
        pay_link = qiwi_pay.create_payment_link()
        if pay_link:
            return pay_link
        return HttpResponseNotFound("hello")

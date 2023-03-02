from django.db import models
from shop.models import Product
from authentication.models import User


class Order(models.Model):
    CONFIRM = 'confirm_pay'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'

    STATUS_RUS = {
        CONFIRM: 'Ожидает оплаты',
        PAID: 'Оплачено',
        OVERDUE: 'Оплата просрочена',
        CANCELLED: 'Отменён',
    }

    STATUS_COLORS = {
        CONFIRM: '#A9A60A',
        PAID: '#008000',
        OVERDUE: '#750606',
        CANCELLED: '#ff0000',
    }

    STATUS_CODES = [
        (CONFIRM, 'Ожидает оплаты'),
        (PAID, 'Оплачено'),
        (OVERDUE, 'Оплата просрочена'),
        (CANCELLED, 'Отменён'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    delivery_adres = models.CharField(max_length=255)
    time_craeted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32,
                              choices=STATUS_CODES,
                              default=CONFIRM)

    def __str__(self):
        return f'{self.id} {self.customer.email}'

    def get_items(self):
        return OrderItem.objects.filter(order__id=self.id)

    def get_status(self):
        return self.STATUS_RUS[self.status]

    def get_color(self):
        return self.STATUS_COLORS[self.status]

    def set_paid(self):
        self.status = self.PAID
        self.save()

    def set_due(self):
        self.status = self.OVERDUE
        self.save()

    def set_cancelled(self):
        self.status = self.CANCELLED
        self.save()

    class Meta:
        verbose_name = 'Заказы пользователей'
        verbose_name_plural = 'Заказы пользователей'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quanity = models.IntegerField(default=1)
    product_price = models.IntegerField()

    def __str__(self):
        return f'{self.order.id} {self.product.vendor_code} \
            {self.product.name}'

    @property
    def amount(self):
        return self.quanity * self.product_price

    class Meta:
        verbose_name = 'Товары заказов'
        verbose_name_plural = 'Товары заказов'

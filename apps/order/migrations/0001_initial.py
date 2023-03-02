# Generated by Django 4.1.6 on 2023-02-08 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('delivery_adres', models.CharField(max_length=255)),
                ('time_craeted', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('confirm_pay', 'Ожидает оплаты'), ('paid', 'Оплачено'), ('overdue', 'Оплата просрочена'), ('cancelled', 'Отменён')], default='confirm_pay', max_length=32)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказы пользователей',
                'verbose_name_plural': 'Заказы пользователей',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quanity', models.IntegerField(default=1)),
                ('product_price', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
            ],
            options={
                'verbose_name': 'Товары заказов',
                'verbose_name_plural': 'Товары заказов',
            },
        ),
    ]
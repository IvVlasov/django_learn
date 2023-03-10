# Generated by Django 4.1.6 on 2023-02-08 19:51

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.Category.get_file_path, verbose_name='Фото категории')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('vendor_code', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Артикул')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('color', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Цвет')),
                ('photo', models.ImageField(upload_to=shop.models.Product.get_file_path, verbose_name='Фото товара')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]

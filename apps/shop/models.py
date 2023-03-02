from django.db import models
from .services.image import resize_image
from django.utils.html import mark_safe


class Category(models.Model):

    def get_file_path(self, filename):
        return f'categories/{self.slug}/{filename}'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name='URL'
    )

    photo = models.ImageField(
        upload_to=get_file_path, verbose_name='Фото категории',
        null=True, blank=True
    )

    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):

    def get_file_path(self, filename):
        return f'{self.category.slug}/{filename}'

    vendor_code = models.CharField(
        max_length=32, primary_key=True, verbose_name='Артикул'
    )
    name = models.CharField(max_length=255, verbose_name='Наименование')
    color = models.CharField(
        max_length=255, default='', verbose_name='Цвет', blank=True, null=True
    )
    photo = models.ImageField(upload_to=get_file_path,
                              verbose_name='Фото товара')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )
    price = models.IntegerField(verbose_name='Цена')

    def save(self, *args, **kwargs):
        self.photo = resize_image(self.photo)
        super(Product, self).save(*args, **kwargs)

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.photo.url}" width="400" height="400"/>'
                )
        return ""

    @property
    def photo_preview_small(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.photo.url}" width="100" height="100" />'
                )
        return ""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

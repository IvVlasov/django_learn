from django.db import models
from shop.models import Category


class Slider(models.Model):

    def get_file_path(self, filename):
        return f'slider/{filename}'

    header = models.CharField(max_length=128, verbose_name='Заголовок',)
    photo = models.ImageField(upload_to=get_file_path,
                              verbose_name='Фото слайдера',
                              null=True,
                              blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдер'

    def __str__(self):
        return self.header


class IndexCats(models.Model):
    name = models.CharField(max_length=120, default='Категории', unique=True)
    left = models.ForeignKey(Category,
                             on_delete=models.SET_NULL,
                             verbose_name='Категория слева',
                             related_name='cat_left',
                             null=True, blank=True)
    right = models.ForeignKey(Category,
                              on_delete=models.SET_NULL,
                              verbose_name='Категория справа',
                              related_name='cat_right',
                              null=True, blank=True)

    class Meta:
        verbose_name = 'Категории на главной странице'
        verbose_name_plural = 'Категории на главной странице'

    def __str__(self):
        return self.name


class Parser(models.Model):
    DNS = 'dns'
    BIGGEEK = 'biggeek'

    SITES = [
        (DNS, 'DNS'),
        (BIGGEEK, 'BIGGEEK'),
    ]

    cat_name = models.CharField(max_length=32,
                                verbose_name='Имя категории')
    cat_slug = models.CharField(max_length=32,
                                verbose_name='URL параметр')
    type = models.CharField(max_length=32,
                            verbose_name='Тип (нужен для парсера)')
    url_slug = models.CharField(max_length=128,
                                verbose_name='URL параметр магазина')
    site_name = models.CharField(max_length=32,
                                 choices=SITES)
    is_active = models.BooleanField(verbose_name='Активно',
                                    default=True)

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Настройки парсера'
        verbose_name_plural = 'Настройки парсера'

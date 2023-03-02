from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ('vendor_code', 'name', 'price', 'color',
                    'category_id', 'photo_preview_small')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        return obj.photo_preview

    def photo_preview_small(self, obj):
        return obj.photo_preview_small

    photo_preview.short_description = 'Фото товара'
    photo_preview.allow_tags = True

    photo_preview_small.short_description = 'Фото товара'
    photo_preview_small.allow_tags = True


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

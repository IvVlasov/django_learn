from django.urls import path

from . import views


urlpatterns = [
    path('<slug:category>/',
         views.ProductListView.as_view(),
         name='shop'),

    path('<slug:category_slug>/<int:pk>',
         views.ProductDetailView.as_view(),
         name='product_detail'),
]

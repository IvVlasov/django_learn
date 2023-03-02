from django.urls import path

from . import views


urlpatterns = [
    path('add/<int:article>',
         views.AddProductView.as_view(),
         name='cart_add'),
    path('remove/<int:article>',
         views.CartRemoveRedirectView.as_view(),
         name='cart_remove'),
    path('update_quantity/<int:article>/<int:quantity>/<str:mode>',
         views.CartUpdateRedirectView.as_view(),
         name='cart_update_quantity'),
    path('details',
         views.cart_page,
         name='cart_page'),

]

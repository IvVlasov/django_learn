from django.urls import path

from . import views


urlpatterns = [
    path('new',
         views.OrderCreateView.as_view(),
         name='new_order'),
    path('all',
         views.OrdersUserListView.as_view(),
         name='orders_all'),
    path('detail/<int:pk>',
         views.OrderUserDetailView.as_view(),
         name='order_detail'),
    path('revoke/<int:pk>',
         views.RevokeOrderView.as_view(),
         name='revoke_order'),

]

from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('registration',
         views.UserCreateView.as_view(),
         name='register_user'),
    path('confirm/<int:pk>',
         views.UserConfirmView.as_view(),
         name='register_confirm'),
    path('sucsess',
         RedirectView.as_view(pattern_name='login'),
         name='register_sucsess'),
    path('login',
         views.UserLoginView.as_view(),
         name='login'),
]

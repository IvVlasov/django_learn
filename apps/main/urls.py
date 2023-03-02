from django.urls import path

from . import views


urlpatterns = [
     path('',
          views.IndexView.as_view(),
          name='index'),
     path('fill_database/',
          views.FillDataAdminView.as_view(),
          name='fill_database'),

]

from django.urls import path

from connectFour import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.api, name='index'),
]


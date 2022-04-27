from django.urls import path

from . import views

urlpatterns = [
    path('', views.apiConnectFourF, name='Api'),
]
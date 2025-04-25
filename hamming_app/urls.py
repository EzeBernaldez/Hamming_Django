from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('response/', views.response, name="response"),
]
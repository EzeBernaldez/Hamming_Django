from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hamming/', views.hamming, name='hamming'),
    path('hamming/hamming-codificar', views.hamming_response, name='hamming-codificar'),
    path('hamming/hamming-decodificar', views.hamming_response_decodificar, name='hamming-decodificar'),
    path('huffman/', views.huffman, name='huffman'), 
    path('huffman/huffman-comprimir', views.huffman_response, name='huffman-comprimir'), 
    path('huffman/huffman-descomprimir', views.huffman_response_descomprimir, name='huffman_response_descomprimir'), 
]
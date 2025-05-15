from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hamming/', views.hamming, name='hamming'),
    path('hamming/hamming_response', views.hamming_response, name='hamming_response'),
    path('huffman/', views.huffman, name='huffman'), 
    path('huffman/huffman_response', views.huffman_response, name='huffman_response'), 
    path('huffman/huffman_response_descomprimir', views.huffman_response_descomprimir, name='huffman_response_descomprimir'), 
]
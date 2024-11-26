from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('books/', views.book_list, name='book_list'),
    path('newspapers/', views.newspaper_list, name='newspaper_list'),
]

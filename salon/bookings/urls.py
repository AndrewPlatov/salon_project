from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_page, name='home'),
    path('my/', views.my, name='my'),
    path('book/', views.book, name='book'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('base/', views.base_page, name='base'),
    path('masters/', views.list_masters, name='list_masters'),
]
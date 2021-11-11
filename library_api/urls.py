from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('all_books/', views.all_books, name='all_books'),
    path('create_record/', views.create_book_record, name='create_book_record'),
]
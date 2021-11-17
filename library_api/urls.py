from django.urls import path
from . import views
# app_name = 'library_api'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('all_books/', views.all_books, name='all_books'),
    path('create_record/', views.create_book_record, name='create_book_record'),
    path('update_record/<pk>', views.update_book_record, name='update_book_record'),
    path('delete_record/<pk>', views.delete_record, name='delete_record'),
    path('author-records/', views.author_books, name='author_books'),
]
from django.db.models import fields
from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('books_name', 'books_img', 'books_description')
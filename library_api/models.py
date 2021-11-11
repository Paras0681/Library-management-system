from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books_name = models.CharField(max_length=255, null=False, blank=False)
    books_img = models.ImageField(upload_to='books_img')
    books_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
         return str(self.books_name)
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Books model which stores books data.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    books_name = models.CharField(max_length=255, null=False, blank=False)
    books_img = CloudinaryField('image')
    books_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
         return str(self.books_name)
# Generated by Django 3.2.9 on 2021-11-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0003_alter_book_books_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='books_img',
            field=models.ImageField(upload_to='books_img'),
        ),
    ]
from django.db import models

# Create your models here.
class Books(models.Model):
    isbn=models.PositiveIntegerField()
    book_name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    published_year=models.PositiveIntegerField()
    book_pic=models.ImageField(upload_to="images",null=True)
    

    def __str__(self):
        return self.book_name
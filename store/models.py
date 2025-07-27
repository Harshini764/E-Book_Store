from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)

    def __str__(self):
        return self.title
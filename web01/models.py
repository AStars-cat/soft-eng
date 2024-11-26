from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    email = models.EmailField()
    company = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)


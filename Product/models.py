from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity= models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username}s cart'
    

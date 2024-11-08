from django.db import models
from django.db.models import Avg


class Category(models.Model):
  
    class Meta:
        verbose_name_plural = 'Categories'
  
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    photographer = models.CharField(max_length=254)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(default='no-image.jpg', null=True, blank=True)
    has_sizes = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

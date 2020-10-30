from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    picture = models.ImageField(upload_to='Product_pics')
    name = models.CharField(max_length=100)
    catagory = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="catagory")
    preview_text = models.TextField(max_length=200)
    details = models.TextField(max_length=500)
    price = models.FloatField()
    old_price = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]

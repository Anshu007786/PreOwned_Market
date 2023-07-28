from django.db import models
from base.models import BaseModel
from django.utils.text import slugify


class Category(BaseModel):
    categoryName = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    categoryImage = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.categoryName)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.categoryName
    

class ColorVarient(BaseModel):
    colorName = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.colorName
    
    


class Product(BaseModel):
    productname = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    productDescription = models.TextField()
    colorVarient = models.ManyToManyField(ColorVarient, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.productname)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.productname

    def getPriceByColor(self, color):
        return self.price + ColorVarient.objects.get(colorName = color).price



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productImages")
    image = models.ImageField(upload_to="product")


class Coupon(BaseModel):
    couponCode = models.CharField(max_length=10)
    isExpired = models.BooleanField(default=False)
    discountPrice = models.IntegerField(default=150)
    minimumAmount = models.IntegerField(default=5000)    
from django.contrib import admin
from .models import Category,Product,ProductImage,ColorVarient,Coupon
# Register your models here.
admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname' , 'price']
    inlines = [ProductImageAdmin]

@admin.register(ColorVarient)
class ColorVarientAdmin(admin.ModelAdmin):
    list_display = ['colorName', 'price']
    model = ColorVarient


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Coupon)
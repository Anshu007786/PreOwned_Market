from django.shortcuts import render, redirect
from .models import Product,ColorVarient

# Create your views here.


def GetProducts(request, slug):
    
    try:
        product = Product.objects.get(slug = slug)
        context = {'product' : product}
        if request.GET.get('color'):
            color = request.GET.get('color')
            price = product.getPriceByColor(color)
            context['selectedColor'] = color
            context['updatedPrice'] = price
            print(price)
        return render(request, "products/products.html", context=context)

    except Exception as e:
        print(e)    


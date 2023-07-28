from django.shortcuts import render
from MarketApp.models import Product
# Create your views here.


def Index(request):

    context = {
        'products' : Product.objects.all()
    }

    return render(request, 'home/index.html', context)

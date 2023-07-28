from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile,Cart,CartItems
from MarketApp.models import Product,ColorVarient,Coupon
import razorpay
# Create your views here.

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'User not found.')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.isEmailVerified:
            messages.warning(request, 'Kindly verify your account')
            return HttpResponseRedirect(request.path_info)

        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect("/")

        messages.warning(request, 'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request, "accounts/login.html")


def RegisterPage(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
      
        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')


def ActivateEmail(request, emailToken):
    try:
        user = Profile.objects.get(emailToken = emailToken)
        user.isEmailVerified = True
        user.save()
        return redirect("/") 
    except Exception as e:
        return HttpResponse("Invalid Token")
    


from django.conf import settings
def cart(request):
    cartObj = None
    payment = None
    try:
        cartObj = Cart.objects.get(isPaid = False, user = request.user)
    except Exception as e:
        print(e)
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        couponObj = Coupon.objects.filter(couponCode__icontains = coupon)
        
        if not couponObj.exists():
            messages.warning(request, 'Invalid Coupon Code')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cartObj.coupon:
            messages.warning(request, 'Coupon Already Applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cartObj.GetCartTotal() < couponObj[0].minimumAmount:
            messages.warning(request, f'Amount should be greater than {couponObj[0].minimumAmount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if couponObj[0].isExpired:
            messages.error(request, 'Coupon Expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        cartObj.coupon = couponObj[0]
        cartObj.save()
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    if cartObj:
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET_KEY))
        payment = client.order.create({'amount' : cartObj.GetCartTotal()*100, 'currency' : 'INR', 'payment_capture' :1})
        cartObj.razorpayOrderID = payment['id']
        cartObj.save()
    
    

    context = {"cart" : cartObj , 'payment' : payment }
    return render(request, "accounts/cart.html", context)



def AddToCart(request, uid):

    varient = request.GET.get('varient')

    product = Product.objects.get(uid = uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user, isPaid = False)

    cartItem = CartItems.objects.create(cart = cart, product = product, )

    if varient:
        varient = request.GET.get('varient')
        colorVarient = ColorVarient.objects.get(colorName = varient)
        print(colorVarient)
        cartItem.colorVariant = colorVarient
        cartItem.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def RemoveCart(request, uid):
    try:
        cartItem = CartItems.objects.get(uid = uid)
        cartItem.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def RemoveCoupon(request,uid):
    cart = Cart.objects.get(uid = uid)
    cart.coupon = None
    cart.save()
    messages.warning(request, 'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Success(request):
    orderID = request.GET.get('order_id')
    cart = Cart.objects.get(razorpayOrderID = orderID)
    cart.isPaid = True
    cart.save()
    return HttpResponse("Payment Successful! Please check your registered email for order details.")


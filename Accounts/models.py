from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import SendAccountActivationEmail
from MarketApp.models import Product,ColorVarient,Coupon

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    isEmailVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=100, null=True, blank=True)
    profileImage = models.ImageField(upload_to="profile")

    def GetCartCount(self):
        return CartItems.objects.filter(cart__isPaid = False, cart__user = self.user).count()



class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    razorpayOrderID = models.CharField(max_length=100, null=True, blank=True)
    razorpayPaymentID = models.CharField(max_length=100, null=True, blank=True)
    razorpayPaymentSignature = models.CharField(max_length=100, null=True, blank=True)

    def GetCartTotal(self):
        cartItems = self.cartItems.all()
        price  = []
        for cartItem in cartItems:
            price.append(cartItem.product.price)
            if cartItem.colorVariant:
                colorVarientPrice = cartItem.colorVariant.price
                price.append(colorVarientPrice)
                
        if self.coupon:
            if self.coupon.minimumAmount < sum(price):
                return sum(price)- self.coupon.discountPrice


        return sum(price)
    
    def CartTotal(self):
        cartItems = self.cartItems.all()
        price  = []
        for cartItem in cartItems:
            price.append(cartItem.product.price)
            if cartItem.colorVariant:
                colorVarientPrice = cartItem.colorVariant.price
                price.append(colorVarientPrice)
                
        return sum(price)



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartItems")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    colorVariant = models.ForeignKey(ColorVarient, on_delete=models.SET_NULL, null=True, blank=True)

    def GetProductPrice(self):
        price = [self.product.price]

        if(self.colorVariant):
            colorVariantPrice = self.colorVariant.price
            price.append(colorVariantPrice)
            
        
        return sum(price)


@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
        
            emailToken = str(uuid.uuid4())
            print(emailToken)
            Profile.objects.create(user = instance , emailToken = emailToken)
            email = instance.email
            SendAccountActivationEmail(email , emailToken)

    except Exception as e:
        print(e)

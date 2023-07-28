from django.urls import path, include
from Accounts.views import LoginPage,RegisterPage,ActivateEmail,cart,Success,AddToCart,RemoveCart,RemoveCoupon


urlpatterns = [
    path('login/', LoginPage, name="Login"),
    path('register/', RegisterPage, name="Register"),
    path('activate/<emailToken>/', ActivateEmail, name="Activate"),
    path('cart/', cart, name="Cart"),
    path('addtocart/<uid>/', AddToCart, name="AddToCart"),
    path('removecart/<uid>/',RemoveCart, name="RemoveCart"),
    path('removecoupon/<uid>/',RemoveCoupon, name="RemoveCoupon"),
    path('success/',Success, name="Success"),
]

from django.contrib import admin
from django.urls import path
from .views import * 
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('payment', auth_middleware(Payment.as_view()), name='payment'),
    path('place-order', auth_middleware(PlaceOrder.as_view()), name='place_order'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('profile', auth_middleware(Profile.as_view()), name='profile'),
    path('change-password', auth_middleware(ChangePassword.as_view()), name='change_password'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('submit-review', SubmitReview.as_view(), name='submit_review'),
    path('search', search, name='search'),
    path('about', about, name='about'),
    path('terms', terms, name='terms'),
    path('privacy', privacy, name='privacy'),
    path('contact', contact, name='contact'),
    path('licence', licence, name='licence'),
]

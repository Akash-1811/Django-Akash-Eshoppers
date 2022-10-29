from django.urls import path
from main import views

urlpatterns = [
    path('index/', views.index),
    path('signup/',views.signup),
    path('login/',views.login,name='login'),
    path('logout/',views.LogoutUser),
    path('cart/',views.cart,name='cart'),
    path('check_out/',views.checkout),
    path('orders/',views.orders,name='order')
]

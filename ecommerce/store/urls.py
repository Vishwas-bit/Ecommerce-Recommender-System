"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from . import views

# from . import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('homepage', views.home, name='homepage'),
# ]

app_name = 'store'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('main/', views.main, name="main"),
    path('login/', views.login_page, name="login"),
    path('store/login/', views.login_page_new, name="login"),
    path('store/logout/',views.logout_page, name="logout"),
    path('register/', views.register, name="register"),
    path('store/', include('django.contrib.auth.urls')),
    path('upload-csv/',views.shop_upload, name="shop_upload"),
    path('upload-csv1/',views.category_upload, name="category_upload"),
    path('upload-csv2/',views.product_upload, name="product_upload"),
    path('upload-csv3/',views.customuser_upload, name="customuser_upload"),
    path('upload-csv4/',views.cartdetail_upload, name="cartdetail_upload"),
    path('search/', views.SearchProductView.as_view(), name='search'),
    path('update_item/', views.updateItem, name='update_item')
    # path('admin/', admin.site.urls),
]

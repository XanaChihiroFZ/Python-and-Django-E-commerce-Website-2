from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

# Initialize the router and register viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

# Define urlpatterns
urlpatterns = [
    # Include the router-generated URLs (API endpoints)
    path('api/', include(router.urls)),

    # Custom paths for your store pages
    path('', views.index, name="index"),
    path('update_item/', views.updateItem, name="update_item"),
    path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart"),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/', views.product, name="product"),
    path('product2/', views.product2, name="product2"),
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("login/authenticate/", login_view, name="login_view"),
    path("signup/register/", signup_view, name="signup_view"),
    path("logout/", logout_view, name="logout"),
    path('terms/', views.terms, name="terms"),
    path('checkout/', views.checkout, name="checkout"), 
    path('checkout/process/', views.process_checkout, name='process_checkout'),
    path('checkout/confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('product/<int:id>/', views.product_details, name='product_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import json
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.

def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order= {'shipping': True}
        cartItems = 0
    context = {'items': items, 'order':order,  'cartItems': cartItems,}
    return render(request, 'webpages/about.html', context)

@login_required(login_url='login')  # Redirect non-authenticated users to login page
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        # Calculate totals using float
        subtotal = sum(float(item.quantity) * float(item.product.price) for item in items)
        tax_rate = 0.05  # Define tax rate as float
        tax = subtotal * tax_rate
        grand_total = subtotal + tax

        # Include item totals
        for item in items:
            item.total_price = float(item.quantity) * float(item.product.price)
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0
        subtotal = 0.0
        tax = 0.0
        grand_total = 0.0
        shipping = False  # Default to False for unauthenticated users


    random_products = Product.objects.order_by('?')[:4]
    
    context = {
        'items': items,
        'order':order,
        'random_products': random_products,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        'cartItems': cartItems,
        'shipping': True,
    }
    return render(request, 'webpages/cart.html', context)


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            # Find the order item
            item = OrderItem.objects.get(id=item_id, order__customer=customer, order__complete=False)
            if item.quantity > 1:
                # Decrement the quantity if it's greater than 1
                item.quantity -= 1
                item.save()
            else:
                # Remove the item completely if quantity is 1
                item.delete()
        except OrderItem.DoesNotExist:
            pass  # Silently ignore if the item doesn't exist
    return redirect('cart')  # Redirect back to the cart page


def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order= {'shipping': True}
        cartItems = 0
        
    trending_products = Product.objects.filter(id__in=[1, 2, 3, 4, 5, 6, 7, 8])  # Fetch first 8 products
    on_sale_products = Product.objects.filter(discount__gt=0)[:4]  # Fetch 4 products with discounts

    context = {
        'trending_products': trending_products,
        'on_sale_products': on_sale_products,
        'cartItems': cartItems,
        'items': items,
        'order':order,
    }
    return render(request, 'webpages/index.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    products = Product.objects.filter(id__in=[1, 2, 3, 4, 5, 6])  # Fetch first 6 products

    context = {'products': products, 'cartItems': cartItems, 'items': items, 'order': order}
    return render(request, 'webpages/product.html', context)


def product2(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    products = Product.objects.filter(id__in=[7, 8, 9, 10, 11, 12])  # Fetch the rest of the products

    context = {'products': products, 'cartItems': cartItems, 'items': items, 'order': order}
    return render(request, 'webpages/product2.html', context)

def login_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'webpages/login.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Fix field name
        password = request.POST.get("password")  # This matches the form

        user = authenticate(username=username, password=password)  # Now using correct username
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

    return render(request, "webpages/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")  # Redirect to home page after logout

def signup_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'webpages/signup.html', context)

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("psw")
        password_repeat = request.POST.get("psw-repeat")

        if password != password_repeat:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Ensure email uniqueness
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

         # Create a Customer instance linked to the new user
        customer = Customer(user=user, email=email)
        customer.save()

        login(request, user)  # Log in the user immediately after signup
        return redirect("index")  # Redirect to home page

    return render(request, "webpages/signup.html")


def terms(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'webpages/terms.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    context = {'items': items, 'order': order, 'cartItems': cartItems, }
    return render(request, 'webpages/checkout.html', context)



@login_required
def process_checkout(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')

        # Get the authenticated customer and their current incomplete order
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()

        if not order:
            # If no active order exists, return to cart or show an error
            return redirect('cart')

        # Save the shipping address
        shipping_address = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zip_code
        )

        # Mark the order as complete
        order.complete = True
        order.save()

        # Redirect to a payment confirmation page
        return redirect('payment_confirmation')

    # If not a POST request, redirect back to checkout
    return redirect('checkout')

def payment_confirmation(request):
    return render(request, 'webpages/payment_confirmation.html')

def product_details(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order= {'shipping': True}
        cartItems = 0  # Default value when the user is not authenticated

    # Fetch the product from the database or return a 404 if not found
    product = get_object_or_404(Product, id=id)
    random_products = Product.objects.order_by('?')[:4]

    context = {
        'product': product,
        'random_products': random_products,
        'cartItems': cartItems,
        'items': items,
        'order': order,
    }
    return render(request, 'webpages/product_details.html', context)



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

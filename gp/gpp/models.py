from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return self.name or "Unnamed Customer"
      
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
	

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)  # Dynamic image field
    discount = models.IntegerField(null=True, blank=True)
	
    def __str__(self):
	    return self.name
	
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        # Set shipping to True if there are any items in the cart
        return self.orderitem_set.exists()

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)


	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
def __str__(self):
        return f"{self.quantity} x {self.product.name}"
	
    
	
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=255, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=20, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		 return f"{self.address}, {self.city}, {self.state} - {self.zipcode}"


    
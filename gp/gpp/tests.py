from django.test import TestCase
from gpp.models import Product, Order, OrderItem, Customer, Category
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Unit Testing: Testing Small Code Components Individually
class OrderModelTest(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        user = User.objects.create_user(username="testuser", password="testpass")
        customer = Customer.objects.create(user=user, email="test@example.com")
        category = Category.objects.create(name="Backpack")  
        product = Product.objects.create(name="Bag", price=50, stock=10, category=category)  # Assign category
        self.order = Order.objects.create(customer=customer, complete=False)
        self.order_item = OrderItem.objects.create(order=self.order, product=product, quantity=2)

    def test_cart_total(self):
        """Test if the cart total is calculated correctly."""
        self.assertEqual(self.order.get_cart_total, 100)  # 50*2 = 100

    def test_cart_items(self):
        """Test if the cart items count is correct."""
        self.assertEqual(self.order.get_cart_items, 2)


# Integration Testing: Testing Components Together
class UserLoginTest(TestCase):
    def setUp(self):
        """Create a test user before running login tests."""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_success(self):
        """Test if a user is redirected to the correct URL after successful login."""
        response = self.client.post("http://127.0.0.1:8000/login/", {"username": "testuser", "password": "testpass"}, follow=True)
        final_url = response.redirect_chain[-1][0] if response.redirect_chain else response.request["PATH_INFO"]
        self.assertEqual(final_url, "http://127.0.0.1:8000")  # Ensure redirect to home page

    def test_login_failure(self):
        """Test if login fails and stays on the login page."""
        response = self.client.post("http://127.0.0.1:8000/login/", {"username": "wronguser", "password": "wrongpass"}, follow=True)
        final_url = response.request["PATH_INFO"]
        self.assertEqual(final_url, "http://127.0.0.1:8000/login/")  # Ensure it remains on login page


# Functional Testing: Automated UI Testing Using Selenium
class FunctionalTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    def test_user_can_login(self):
        """Test if a user can log in via the UI."""
        self.driver.get("http://127.0.0.1:8000/login/")

        # Wait for the username input to appear
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")

        # Enter credentials
        username_field.send_keys("sauce")
        password_field.send_keys("packetforsale0")

        # Click login
        login_button.click()

        # Wait for redirect and verify successful login
        time.sleep(5)  # Adjust based on response speed
        self.assertIn("http://127.0.0.1:8000", self.driver.current_url)  # Ensure correct redirection

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

class SecurityTest(TestCase):
    def test_user_creation(self):
        """Ensure a user can be created."""
        user = User.objects.create_user(username="testuser", password="testpass")
        self.assertTrue(User.objects.filter(username="testuser").exists())

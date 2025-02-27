from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
import string

class CustomUserManager(BaseUserManager):
    """ Custom manager for user model where email is the unique identifier """
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email.split('@')[0])  # Default username
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # No restriction on password length
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CLIENT', 'Client'),
        ('SERVICE_PROVIDER', 'Service Provider'),
        ('NORMAL_USER', 'Normal user'),
    ]

    email = models.EmailField(unique=True)  # Ensure email is unique
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True , default='profile_pics/profile.png')
    created_at = models.DateTimeField(auto_now_add=True)

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)  # Not required
    USERNAME_FIELD = 'email'  # Login using email
    REQUIRED_FIELDS = []  # Don't require username

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)  # e.g., Laundry, Plumbing, Babysitting
    description = models.TextField()
    icon = models.ImageField(upload_to='category_icons/', null=True)
    
    class Meta:
        verbose_name_plural = "Service Categories"
    
    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    bio = models.TextField()
    experience_years = models.PositiveIntegerField()
    id_number = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0.0)
    total_jobs = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name}"

class LaundryPricing(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    basket_size = models.CharField(max_length=50)  # Small, Medium, Large
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()  # What's included in this basket size
    
    class Meta:
        unique_together = ('service_provider', 'basket_size')
    
    def __str__(self):
        return f"{self.service_provider.user.username} - {self.basket_size}"

class ServiceVideo(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='service_videos/')
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_instructions = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.client.username} with {self.service_provider.user.username}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('CARD', 'Credit/Debit Card'),
        ('CASH', 'Cash'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    paid_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Booking {self.booking.id}"
    



# E-commerce Models


from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class PickupStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    details = models.TextField()
    
    def __str__(self):
        return self.name


# Ensure you're referencing the custom User model
User = get_user_model()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='sellers/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, blank=True, null=True)

    score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    followers = models.ManyToManyField(User, related_name='followed_sellers', blank=True)

    def __str__(self):
        return self.store_name

    @property
    def followers_count(self):
        return self.followers.count()

    # Automatically generate slug from store_name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)



class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Ensure uniqueness

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Make name unique if desired
    slug = models.SlugField(unique=True)  # Make slug unique and required
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # If the slug is not set, create it from the name field
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from decimal import Decimal

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products" , null=True, blank=True)
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sponsored = models.BooleanField(default=False)  # Add this field
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_official = models.BooleanField(default=False)  # For "official store" badge
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)  # Add this field
    currency = models.CharField(max_length=10, default="KES")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_in_stock = models.BooleanField(default=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_time = models.CharField(max_length=100, null=True, blank=True)
    pay_on_delivery = models.BooleanField(default=False)
    return_policy_short = models.TextField(null=True, blank=True)
    pickup_days = models.PositiveIntegerField(default=0)  # Number of days for pickup
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = uuid.uuid4().hex[:6]  # Generates a unique 6-character string
            self.slug = slugify(f"{self.name}-{unique_id}")

        # Calculate original price based on discount percentage
        if self.discount_percentage and self.discount_percentage > 0:
            # Convert the discount calculation to Decimal to avoid type errors
            discount_factor = Decimal('1') - (Decimal(self.discount_percentage) / Decimal('100'))
            self.original_price = (self.price / discount_factor).quantize(Decimal('0.01'))
        else:
            # If no discount, original price is the same as price
            self.original_price = self.price

        super().save(*args, **kwargs)

       

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Feature(models.Model):
    product = models.ForeignKey(Product, related_name="features", on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature


class Specification(models.Model):
    product = models.ForeignKey(Product, related_name="specifications", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label}: {self.value}"


class Product_Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pickup_station = models.ForeignKey(PickupStation, on_delete=models.SET_NULL, null=True, blank=True)
    
    order_id = models.CharField(max_length=6, unique=True, default='')
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            characters = string.ascii_uppercase + string.digits
            while True:
                new_id = ''.join(random.choice(characters) for _ in range(6))
                if not Order.objects.filter(order_id=new_id).exists():
                    self.order_id = new_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
       return f"Order {self.order_id}"
    
    
    @property
    def get_cart_total(self):
        orderitems = self.items.all()  # Changed from orderitem_set to items
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_order_total(self):
        return self.get_cart_total + self.delivery_fee
    
    @property
    def get_total_items(self):
        orderitems = self.items.all()  # Changed from orderitem_set to items
        return sum([item.quantity for item in orderitems])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    vendor = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date_start = models.DateField(null=True, blank=True)
    delivery_date_end = models.DateField(null=True, blank=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"




class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_order_items_display(self):
        items = self.order.items.all()
        if not items:
            return "No items"
        
        item_strings = [f"{item.quantity} x {item.product.name}" for item in items]
        return ", ".join(item_strings)
    
    def __str__(self):
        items_summary = self.get_order_items_display()
        return f"Transaction {self.id} - {self.user.username} ({items_summary})"
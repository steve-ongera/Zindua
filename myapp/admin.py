from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'role', 'location', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'role', 'location', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'role', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

# Service Category Admin
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(ServiceCategory, ServiceCategoryAdmin)

# Service Provider Admin
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'experience_years', 'is_verified', 'total_jobs')
    list_filter = ('is_verified', 'category')
    search_fields = ('user__email', 'id_number')

admin.site.register(ServiceProvider, ServiceProviderAdmin)

# Laundry Pricing Admin
class LaundryPricingAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'basket_size', 'price')
    list_filter = ('service_provider',)
    search_fields = ('service_provider__user__email', 'basket_size')

admin.site.register(LaundryPricing, LaundryPricingAdmin)

# Service Video Admin
class ServiceVideoAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'title', 'uploaded_at', 'views')
    list_filter = ('uploaded_at',)
    search_fields = ('title',)

admin.site.register(ServiceVideo, ServiceVideoAdmin)

# Booking Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'service_provider', 'service_date', 'status', 'total_price')
    list_filter = ('status', 'service_date')
    search_fields = ('client__email', 'service_provider__user__email')

admin.site.register(Booking, BookingAdmin)

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    search_fields = ('booking__client__email', 'booking__service_provider__user__email')

admin.site.register(Review, ReviewAdmin)

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'booking__client__email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__email', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

admin.site.register(Payment, PaymentAdmin)



class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')  # Customize the fields to display in the admin list view
    prepopulated_fields = {'slug': ('name',)}  # Automatically generate the slug based on the name

admin.site.register(Subcategory, SubcategoryAdmin)



@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'contact_email', 'phone_number')  # Fields to display in the admin list view
    search_fields = ('store_name', 'user__username', 'contact_email')  # Searchable fields
    prepopulated_fields = {'slug': ('store_name',)}  # Auto-generate slug from store name
    list_filter = ('store_name',)  # Add filters for quick filtering


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')  # Display product and image in the admin list view
    search_fields = ('product__name',)  # Enable search functionality by product name

# Register ProductImage model with the admin site
admin.site.register(ProductImage, ProductImageAdmin)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature')  # Display product and feature in the admin list view
    search_fields = ('product__name', 'feature')  # Enable search functionality by product name and feature

# Register Feature model with the admin site
admin.site.register(Feature, FeatureAdmin)
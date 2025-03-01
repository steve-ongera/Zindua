# context_processors.py

from django.db.models import Sum  # Import Sum from Django ORM
from django.db.models import Sum, Count
from .models import Cart, CartItem  # Adjust the import according to your app structure

def navbar_context(request):
    """Context processor to include main categories and cart item count."""

    # Fetch top 5 categories with most products
    # Assuming Category has a related_name 'products' to its Product model
    main_categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:5]
    
    # Convert QuerySet to list of dictionaries for template
    main_categories = [
        {'name': category.name, 'slug': category.slug}
        for category in main_categories
    ]
    
    cart_items_count = 0
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            # Count total quantity of items in the cart
            cart_items_count = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        except Cart.DoesNotExist:
            cart_items_count = 0
    
    return {
        'main_categories': main_categories,
        'cart_items': cart_items_count
    }



from myapp.models import Category

def categories_processor(request):
    categories = Category.objects.all()
    # Optional: Filter out categories with no slug
    categories = categories.exclude(slug="")
    return {'categories': categories}

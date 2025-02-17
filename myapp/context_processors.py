# context_processors.py

def navbar_context(request):
    """Context processor to include main categories in every template."""
    # Example data, you would typically fetch this from your database
    main_categories = [
        {'name': 'Supermarket', 'slug': 'supermarket'},
        {'name': 'Health & Beauty', 'slug': 'health-beauty'},
        {'name': 'Home & Office', 'slug': 'home-office'},
        {'name': 'Phones & Tablets', 'slug': 'phones-tablets'},
        {'name': 'Computing', 'slug': 'computing'},
        {'name': 'Electronics', 'slug': 'electronics'},
        {'name': 'Fashion', 'slug': 'fashion'},
    ]
    
    # Get cart items count from session or user model
    cart_items = request.session.get('cart_items_count', 0)
    
    return {
        'main_categories': main_categories,
        'cart_items': cart_items
    }
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Avg 
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your actual home page
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def custom_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email_or_username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to dashboard
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def home_view(request):
    categories = ServiceCategory.objects.all()
    top_providers = ServiceProvider.objects.order_by('-average_rating')[:8]
    sponsored_products = Product.objects.filter(is_sponsored=True)[:10]  # Example, modify as needed

    product_categories = Category.objects.all()
    top_sold_products = Product.objects.order_by('-stock')[:10]  # Example: Replace 'stock' with actual sales tracking field
    top_selling_products = Product.objects.order_by('-sales_count')[:6]  


    context = {
        'categories': categories,
        'top_providers': top_providers,
        'sponsored_products': sponsored_products,
        'product_categories': product_categories,
        'top_sold_products': top_sold_products,
        'top_selling_products': top_selling_products,
    }
    return render(request, 'home.html', context)

def product_list_view(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'e-commerce/product_list.html', {'page_obj': page_obj})

@login_required
def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    seller = product.seller  # Assuming Product has a ForeignKey to Seller

    #recently views using sessions 
    # Initialize the recently viewed products list in session if not present
    recently_viewed = request.session.get('recently_viewed', [])

    # Add the current product's slug if it's not already in the list
    if product.slug not in recently_viewed:
        recently_viewed.append(product.slug)

    # Limit the list to, for example, 5 products
    if len(recently_viewed) > 5:
        recently_viewed.pop(0)

    # Save the updated recently viewed list in the session
    request.session['recently_viewed'] = recently_viewed

    # Fetch a default set of products if the list is empty
    if not recently_viewed:
        default_products = Product.objects.all()[:5]  # Or any criteria for default products
    else:
        default_products = Product.objects.filter(slug__in=recently_viewed)

    # Get the features of the product
    features = Feature.objects.filter(product=product)

    # Get other related objects (optional, as needed)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]  # Adjust the filter based on your needs
    sponsored_products = Product.objects.filter(is_sponsored=True)[:5]  # Example, modify as needed
    
    context = {
        'product': product,
        'features': features,
        'related_products': related_products,
        'sponsored_products': sponsored_products,
        'recently_viewed': default_products,
        'seller': seller
    }

    return render(request, 'e-commerce/product_detail.html' , context)
    


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    # Apply Pagination (12 Products Per Page)
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number)

    return render(request, 'category.html', {
        'category': category,
        'products': paginated_products  # Use paginated products in template
    })


def brand_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)
    return render(request, 'brand.html', {'brand': brand, 'products': products})


def account_view(request):
    # Example: You can pass user information like username and email to the template
    user = request.user
    return render(request, 'account.html', {'user': user})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('cart')  # Ensure this exists in `urls.py`

def cart_view(request):
    # Assuming you have a Cart model or you're using the session to store cart items
    cart_items = request.session.get('cart', [])
    
    # Optionally, if you have a Cart model and want to calculate the total items:
    total_items = len(cart_items)
    
    return render(request, 'cart.html', {'cart_items': total_items})

def seller_profile(request, slug):
    seller = get_object_or_404(Seller, slug=slug)
    return render(request, 'seller_profile.html', {'seller': seller})

def search_view(request):
    query = request.GET.get('q', '')
    if query:
        # Assuming you have a Product model, adjust to your actual model
        results = Product.objects.filter(name__icontains=query)  # Adjust field name as needed
    else:
        results = Product.objects.all()  # Return all if no query
    
    return render(request, 'search_results.html', {'results': results, 'query': query})


def service_provider_list(request):
    category = request.GET.get('category')
    if category:
        providers = ServiceProvider.objects.filter(category__name=category)
    else:
        providers = ServiceProvider.objects.all()
    
    context = {
        'providers': providers
    }
    return render(request, 'service_providers_list.html', context)

def service_provider_detail(request, pk):
    provider = get_object_or_404(ServiceProvider, pk=pk)
    pricing = LaundryPricing.objects.filter(service_provider=provider)
    videos = ServiceVideo.objects.filter(service_provider=provider)
    reviews = Review.objects.filter(
        booking__service_provider=provider
    ).order_by('-created_at')
    
    context = {
        'provider': provider,
        'pricing': pricing,
        'videos': videos,
        'reviews': reviews
    }
    return render(request, 'service_provider_detail.html', context)

@login_required
def book_service(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.service_provider = provider
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking_form.html', {
        'form': form,
        'provider': provider
    })

@login_required
def profile_view(request):
    if hasattr(request.user, 'serviceprovider'):
        return redirect('provider_dashboard')
    bookings = Booking.objects.filter(client=request.user)
    return render(request, 'profile.html', {'bookings': bookings})

@login_required
def provider_dashboard(request):
    provider = request.user.serviceprovider
    bookings = Booking.objects.filter(service_provider=provider)
    return render(request, 'provider_dashboard.html', {
        'provider': provider,
        'bookings': bookings
    })

# Additional useful views for the application

@login_required
def create_service_provider_profile(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('provider_dashboard')
    else:
        form = ServiceProviderForm()
    
    return render(request, 'create_provider_profile.html', {'form': form})

@login_required
def add_pricing(request):
    if not hasattr(request.user, 'serviceprovider'):
        return redirect('home')
        
    if request.method == 'POST':
        form = LaundryPricingForm(request.POST)
        if form.is_valid():
            pricing = form.save(commit=False)
            pricing.service_provider = request.user.serviceprovider
            pricing.save()
            return redirect('provider_dashboard')
    else:
        form = LaundryPricingForm()
    
    return render(request, 'add_pricing.html', {'form': form})

@login_required
def upload_service_video(request):
    if not hasattr(request.user, 'serviceprovider'):
        return redirect('home')
        
    if request.method == 'POST':
        form = ServiceVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.service_provider = request.user.serviceprovider
            video.save()
            return redirect('provider_dashboard')
    else:
        form = ServiceVideoForm()
    
    return render(request, 'upload_video.html', {'form': form})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            
            # Update provider's average rating
            provider = booking.service_provider
            avg_rating = Review.objects.filter(
                booking__service_provider=provider
            ).aggregate(Avg('rating'))['rating__avg']
            provider.average_rating = avg_rating
            provider.save()
            
            return redirect('booking_detail', booking_id=booking_id)
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {
        'form': form,
        'booking': booking
    })
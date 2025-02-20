# urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),


    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
 

    path('providers/', views.service_provider_list, name='provider_list'),
    path('provider/<int:pk>/', views.service_provider_detail, name='provider_detail'),
    path('book/<int:provider_id>/', views.book_service, name='book_service'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('create-provider-profile/', views.create_service_provider_profile, name='create_provider_profile'),
    path('add-pricing/', views.add_pricing, name='add_pricing'),
    path('upload-video/', views.upload_service_video, name='upload_video'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('add-review/<int:booking_id>/', views.add_review, name='add_review'),

    #e-commerce
    path('products/', views.product_list_view, name='product_list'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('account/', views.account_view, name='account'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
    path('pay/', views.pay_view, name='pay'),
    path('order-success/', views.order_success, name='order_success'),
    path('orders/', views.orders_view, name='orders'),
    

    path('category/<slug:slug>/', views.category_view, name='category'),
    path('brand/<slug:slug>/', views.brand_view, name='brand'),
    path('seller/<slug:slug>/', views.seller_profile, name='seller_profile'),

    ## Other URL patterns admin urls
    
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),

]
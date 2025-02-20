# Jumia E-commerce Clone

![Jumia Logo](https://static.jumia.co.ke/cms/2023/W01/HP/Desktop/JumiaLogo.png)

## Overview

This Django-based e-commerce platform is a clone of Jumia, Africa's leading online marketplace. It provides a comprehensive shopping experience with features for product browsing, cart management, user accounts, and order processing. The application is designed to be responsive, scalable, and user-friendly, catering to both customers and administrators.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Authentication](#authentication)
- [Payment Integration](#payment-integration)
- [Admin Dashboard](#admin-dashboard)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

### Customer Features
- **User Authentication & Profile Management**
  - Registration, login, password recovery
  - Address book management
  - Order history tracking
  - Wishlist creation and management

- **Product Browsing & Searching**
  - Category-based navigation
  - Advanced search with filters (price, brand, rating)
  - Product sorting (newest, price, popularity)
  - Detailed product pages with specifications, reviews, related items

- **Shopping Experience**
  - Shopping cart management
  - Save for later functionality
  - Product comparison
  - Recently viewed products tracking

- **Checkout Process**
  - Multi-step checkout (address, delivery, payment)
  - Pickup station selection
  - Multiple payment methods (M-Pesa, card, bank transfer)
  - Promocode/voucher application
  - Order review and confirmation

- **Post-Purchase**
  - Order tracking
  - Delivery status notifications
  - Return/refund request processing
  - Product review submission

### Seller Features
- Seller registration and dashboard
- Product listing and inventory management
- Order fulfillment
- Analytics and reporting

### Admin Features
- Comprehensive admin dashboard
- User management
- Product and category management
- Order processing and reporting
- Promotion and discount management

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Search Engine**: Elasticsearch (optional)

### Frontend
- **Template Engine**: Django Templates with HTMX
- **CSS Framework**: Custom CSS with Tailwind CSS
- **JavaScript**: Vanilla JS with some Alpine.js components
- **UI Components**: Custom components matching Jumia's design

### APIs & Integrations
- **Payment**: M-Pesa, Stripe, Flutterwave
- **SMS**: Africa's Talking
- **Email**: SendGrid/Mailgun
- **Maps**: Google Maps API (for delivery tracking)
- **Storage**: AWS S3 (for product images and assets)

## System Requirements

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (for frontend asset compilation)
- Git

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/steve-ongera/Zindua.git
   cd Zindua
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   npm install  # For frontend assets
   ```

4. **Set up environment variables**
   - Create a `.env` file based on `.env.example`
   ```bash
   cp .env.example .env
   # Edit the .env file with your configuration
   ```

5. **Set up the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial data (optional)**
   ```bash
   python manage.py loaddata fixtures/categories.json
   python manage.py loaddata fixtures/products.json
   ```

8. **Compile static assets**
   ```bash
   npm run build
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main site: http://localhost:8000
    - Admin dashboard: http://localhost:8000/admin

## Project Structure

```
jumia-ecommerce/
├── accounts/            # User authentication and profiles
├── api/                 # API endpoints
├── cart/                # Shopping cart functionality
├── checkout/            # Checkout process
├── core/                # Core functionality and settings
├── dashboard/           # Admin and seller dashboards
├── media/               # User-uploaded content
├── orders/              # Order processing
├── payments/            # Payment integrations
├── products/            # Product catalog and management
├── reviews/             # Product reviews
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/           # HTML templates
├── utils/               # Utility functions
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
├── manage.py            # Django management script
├── package.json         # Frontend dependencies
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Database Schema

### Main Entities

#### User & Authentication
- **User**: Extended Django User model
- **Address**: User addresses
- **Seller**: Seller-specific profile
- **Staff**: Staff members with role-based permissions

#### Product Catalog
- **Category**: Hierarchical product categories
- **Brand**: Product brands
- **Product**: Core product information
- **ProductVariant**: Size, color, and other variants
- **ProductSpecification**: Technical specifications
- **ProductImage**: Product images
- **Inventory**: Stock tracking

#### Shopping & Orders
- **Cart**: Shopping cart
- **CartItem**: Items in cart
- **Order**: Customer orders
- **OrderItem**: Items in an order
- **Shipment**: Shipping arrangements
- **Pickup**: Pickup station details
- **Payment**: Payment information
- **Refund**: Refund requests

#### Supporting Entities
- **Review**: Product reviews
- **Rating**: Product ratings
- **Wishlist**: User wishlists
- **Coupon**: Discount coupons
- **Promotion**: Special offers
- **SearchLog**: User search history
- **BrowsingHistory**: Recently viewed products

## API Endpoints

### Authentication
- `POST /api/auth/register/`: User registration
- `POST /api/auth/login/`: User login
- `POST /api/auth/logout/`: User logout
- `POST /api/auth/password-reset/`: Password reset

### User Profile
- `GET /api/profile/`: Get user profile
- `PUT /api/profile/`: Update user profile
- `GET /api/profile/addresses/`: List user addresses
- `POST /api/profile/addresses/`: Add address

### Products
- `GET /api/products/`: List products
- `GET /api/products/{id}/`: Get product details
- `GET /api/categories/`: List categories
- `GET /api/brands/`: List brands

### Cart
- `GET /api/cart/`: Get cart items
- `POST /api/cart/`: Add item to cart
- `PUT /api/cart/{id}/`: Update cart item
- `DELETE /api/cart/{id}/`: Remove item from cart

### Orders
- `GET /api/orders/`: List user orders
- `POST /api/orders/`: Create order
- `GET /api/orders/{id}/`: Get order details
- `POST /api/orders/{id}/pay/`: Process payment

### Reviews
- `GET /api/products/{id}/reviews/`: Get product reviews
- `POST /api/products/{id}/reviews/`: Add product review

## Frontend Components

### Page Templates
- **Homepage**: Featured products, categories, and promotions
- **Category Page**: Products by category with filters
- **Product Detail**: Full product information and actions
- **Shopping Cart**: Cart management
- **Checkout**: Address, delivery, and payment steps
- **Order Confirmation**: Order summary and next steps
- **User Dashboard**: Profile, orders, and preferences

### Reusable Components
- Navigation menu with megamenu
- Product card/grid/list views
- Category browser
- Filter and sort controls
- Image gallery/carousel
- Review form and display
- Alert and notification system
- Responsive tables
- Form components
- Loading indicators

## Authentication

The system uses Django's authentication framework with extensions for:
- Social authentication (Google, Facebook)
- Two-factor authentication (optional)
- JWT for API authentication
- Custom user model with extended fields

## Payment Integration

### M-Pesa Integration
- STK Push for direct payments
- C2B integration for merchant payments
- Transaction validation and confirmation
- Detailed transaction reporting

### Other Payment Methods
- Credit/debit card processing via Stripe
- Mobile money via Flutterwave
- Bank transfers
- Pay on delivery

### Implementation Guide
1. Configure the payment gateway credentials in `.env`
2. Process payments using the `payments` app
3. Handle webhooks for payment confirmations
4. Store transaction records securely

## Admin Dashboard

The admin dashboard includes:
- **Analytics**: Sales, traffic, conversion metrics
- **Order Management**: Processing, tracking, cancellations
- **Product Management**: Add, edit, remove products
- **User Management**: Customer accounts and permissions
- **Content Management**: Banners, promotions, featured products
- **Inventory Management**: Stock levels and alerts
- **Reports**: Sales, customer, product performance reports

## Deployment

### Production Deployment

#### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t jumia-ecommerce .
   ```

2. Run the container:
   ```bash
   docker-compose up -d
   ```

#### Traditional Deployment
1. Set up a production server (Ubuntu 20.04+ recommended)
2. Install required dependencies
3. Set up a web server (Nginx) and application server (Gunicorn)
4. Configure PostgreSQL for production
5. Set up SSL certificates
6. Configure static file serving
7. Set up backup and monitoring

#### Deployment Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS and HSTS
- [ ] Configure database connection pooling
- [ ] Set up media file storage with AWS S3
- [ ] Configure caching with Redis
- [ ] Set up Celery for background tasks
- [ ] Configure email settings for transactional emails
- [ ] Set up logging and error tracking
- [ ] Configure database backups

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test products

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Categories
- **Unit Tests**: Testing individual functions and methods
- **Integration Tests**: Testing interactions between components
- **API Tests**: Testing API endpoints
- **UI Tests**: Testing user interfaces (using Selenium)
- **Performance Tests**: Load testing critical pages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use Django's style guide for templates
- Document functions and classes properly
- Write tests for new features
- Keep the code modular and DRY

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/) - The web framework used
- [Jumia](https://www.jumia.co.ke/) - Inspiration for the interface and features
- [Tailwind CSS](https://tailwindcss.com/) - For responsive styling
- [HTMX](https://htmx.org/) - For interactive features
- [Font Awesome](https://fontawesome.com/) - For icons
- All contributors who participated in this project
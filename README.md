# GP Store: Django E-Commerce Website

A full-stack e-commerce web application built with **Python** and **Django**, featuring product browsing, a shopping cart, user authentication, checkout, and a REST API layer for products and categories.

> **Client Project Notice:** This application was built as freelance/contract work for a client. It is shared here as a portfolio piece to demonstrate development skills. It is a second iteration of an earlier project, [Python-and-Django-E-commerce-Website](https://github.com/XanaChihiroFZ/Python-and-Django-E-commerce-Website), refined with additional features such as a REST API, discount/sale logic, and a more complete checkout flow.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Libraries & Packages](#libraries--packages)
3. [Skills Demonstrated](#skills-demonstrated)
4. [Project Structure](#project-structure)
5. [File-by-File Breakdown](#file-by-file-breakdown)
6. [How It Works](#how-it-works)
7. [Data Models](#data-models)
8. [Setup & Installation](#setup--installation)
9. [Notes / Future Improvements](#notes--future-improvements)
10. [Acknowledgment](#acknowledgment)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Django 5.1 |
| API Layer | Django REST Framework (DRF) |
| Database | SQLite3 (Django's default dev database) |
| Frontend | Django Templates (HTML5), CSS3, vanilla JavaScript |
| Auth | Django's built-in authentication system (`django.contrib.auth`) |
| Static/Media Files | Django's static & media file handling |

## Libraries & Packages

- **Django**; core web framework (models, views, templates, URL routing, admin panel, auth, ORM).
- **djangorestframework (DRF)**; powers the `/api/` endpoints for `Product` and `Category` using `ModelViewSet` and `DefaultRouter`.
- **django.contrib.auth**; handles user accounts, login/logout, and password validation.
- **json** (standard library); used to parse the AJAX request body for the "add/remove from cart" action.
- **Vanilla JavaScript** (`cart.js`, `index.js`, `slider.js`); handles client-side interactivity (cart quantity updates via `fetch`/AJAX, homepage behavior, image sliders).
- **zoomsl.min.js**; a third-party, minified JavaScript plugin used to give product images a zoom-on-hover effect on the product detail page.
- **Glide.js**; a lightweight third-party carousel library that powers the homepage hero banner slider (`slider.js` initializes it on `#glide_1`).
- **Selenium** (`selenium.webdriver`); a browser-automation library used in `tests.py` to drive a real Chrome browser for end-to-end UI testing (e.g., simulating a user typing credentials and clicking "Login").
- **Boxicons** (loaded via CDN in `base.html`); an icon font library used for the header, search, cart, and footer social icons.

## Skills Demonstrated

- Designing a relational database schema (Customer, Category, Product, Order, OrderItem, ShippingAddress) with Django's ORM, including `ForeignKey`, `OneToOneField`, `@property` calculated fields, and `on_delete` behaviors.
- Building both a **server-rendered website** (Django templates) and a **REST API** (Django REST Framework) in the same project.
- Implementing user authentication and authorization from scratch (custom signup/login views, `@login_required` decorators, session-based auth) rather than relying only on Django's default auth views.
- Building a stateful shopping cart: creating an "incomplete" `Order` per customer, adding/removing `OrderItem`s via AJAX, and calculating subtotal, tax, and grand total.
- Handling a multi-step checkout flow: cart → shipping details form → order completion → confirmation page.
- Working with Django's static and media file configuration to serve CSS, JS, and product images.
- Structuring a Django project using the standard **project/app** split (`gp` project, `gpp` app).
- Writing clean, RESTful URL routing with DRF's `DefaultRouter` alongside traditional Django `path()` routes in the same `urls.py`.
- Front-end skills: responsive page templates, an image slider/carousel, and a product image zoom effect.
- **Automated testing at multiple levels**: unit tests for model logic (cart totals), integration tests for the login flow via Django's test client, and functional/end-to-end UI tests driving a real browser with Selenium.

## Project Structure

```
gp/
├── manage.py                     # Django's command-line utility (runserver, migrate, etc.)
├── db.sqlite3                    # SQLite database file (auto-generated)
│
├── gp/                            # Project-level configuration package
│   ├── __init__.py
│   ├── settings.py                # Project settings (apps, database, static/media config)
│   ├── urls.py                    # Root URL routing; delegates to the gpp app
│   ├── asgi.py                    # ASGI entry point (async server support)
│   └── wsgi.py                    # WSGI entry point (traditional server support)
│
├── gpp/                            # Main Django app ("store" app)
│   ├── __init__.py
│   ├── admin.py                    # Registers models with the Django admin panel
│   ├── apps.py                     # App configuration
│   ├── models.py                   # Database models (Customer, Product, Order, etc.)
│   ├── serializers.py              # DRF serializers (Product, Category) for the REST API
│   ├── views.py                    # Page views + API viewsets (business logic)
│   ├── urls.py                     # App-level routes (pages + /api/ endpoints)
│   ├── tests.py                    # Placeholder for unit tests
│   ├── migrations/                 # Auto-generated DB schema migration files
│   └── templates/
│       ├── base.html               # Shared layout (navbar, footer, cart icon, etc.)
│       └── webpages/
│           ├── index.html              # Homepage (trending + on-sale products)
│           ├── product.html            # Product listing page 1
│           ├── product2.html           # Product listing page 2
│           ├── product_details.html    # Single product detail page
│           ├── cart.html               # Shopping cart page
│           ├── checkout.html           # Checkout / shipping form
│           ├── payment_confirmation.html # Order confirmation page
│           ├── login.html              # Login page
│           ├── signup.html             # Registration page
│           ├── about.html              # About page
│           └── terms.html              # Terms & conditions page
│
└── static/
    ├── css/
    │   └── styles.css              # Site-wide styling
    ├── js/
    │   ├── cart.js                 # AJAX add/remove-from-cart logic
    │   ├── index.js                # Homepage interactivity
    │   ├── slider.js                # Banner/image carousel logic
    │   └── zoomsl.min.js            # Third-party product image zoom plugin
    └── images/                      # Banners, category icons, and product photos
```

## File-by-File Breakdown

### Project config (`gp/gp/`)
- **`settings.py`**; Registers the `gpp` app and `rest_framework`; configures SQLite as the database, sets `STATIC_URL`/`STATICFILES_DIRS` for CSS/JS/images, and `MEDIA_URL`/`MEDIA_ROOT` for uploaded product images.
- **`urls.py`**; The root router. It only does one thing: forward every URL into `gpp.urls`, plus expose `/admin/`.
- **`wsgi.py` / `asgi.py`**; Standard Django deployment entry points (sync and async servers, respectively). Not customized beyond Django's defaults.

### App core (`gp/gpp/`)
- **`models.py`**; Defines the database schema (see [Data Models](#data-models) below).
- **`serializers.py`**; Converts `Product` and `Category` model instances to/from JSON for the REST API, using DRF's `ModelSerializer` with `fields = '__all__'`.
- **`views.py`**; Contains both:
  - **Page views** (return rendered HTML): `index`, `about`, `cart`, `product`, `product2`, `product_details`, `login_page`, `signup_page`, `terms`, `checkout`, `payment_confirmation`.
  - **Action views** (handle form submissions / AJAX, then redirect or return JSON): `login_view`, `signup_view`, `logout_view`, `updateItem`, `remove_from_cart`, `process_checkout`.
  - **API viewsets** (`ProductViewSet`, `CategoryViewSet`): DRF `ModelViewSet`s that auto-generate full CRUD REST endpoints.
- **`urls.py`**; Combines two routing styles in one file:
  - A DRF `DefaultRouter` registered under `/api/` for `products` and `categories` (auto-generates list/detail/create/update/delete endpoints).
  - Standard Django `path()` routes for every page (home, cart, login, signup, checkout, etc.).
- **`admin.py`**; Registers all six models (`Product`, `Category`, `Customer`, `Order`, `OrderItem`, `ShippingAddress`) with `admin.site.register()`, so store staff can view and edit every table from Django's built-in `/admin/` panel.
- **`apps.py`**; The `GppConfig` app configuration class Django uses to identify and load the `gpp` app; sets `BigAutoField` as the default primary key type.
- **`tests.py`**; A real, multi-level test suite covering:
  - **Unit tests** (`OrderModelTest`); verify `Order.get_cart_total` and `get_cart_items` compute correctly against a Customer/Product/Order fixture.
  - **Integration tests** (`UserLoginTest`); use Django's test client to POST to `/login/` and confirm success redirects home and failure stays on the login page.
  - **Functional/E2E tests** (`FunctionalTest`); drive an actual Chrome browser with Selenium to fill in the login form and click the submit button, verifying the real UI flow works end-to-end.
  - **Security test** (`SecurityTest`); confirms a `User` is correctly created and persisted.
- **`migrations/0001_initial.py`**; The migration file Django generated from `models.py`; it's the actual SQL blueprint used to build `db.sqlite3`.

### Templates (`gp/gpp/templates/`)
- **`base.html`**; The shared page shell that every other template extends via `{% block content %}`. It defines:
  - A top contact bar (phone number and email) and the main navigation bar, branded "Green Plants" with a logo, links to Home, Shop, Terms, About, and Contact.
  - Header icons for account/login, search, and cart; the cart icon shows a live item count via `{{cartItems}}`, and a "Log Out" link appears only when `user.is_authenticated`.
  - A mobile hamburger menu toggle (wired up in `index.js`).
  - A small inline script that reads the Django CSRF cookie into a `csrftoken` JavaScript variable and stores the current user in a `user` variable; both are used by `cart.js` when it makes AJAX requests.
  - A shared "Excellent Support" contact section and a footer with informational links (About, Contact, Terms, Shipping Guide), quick links, and social icons via Boxicons.
  - Two extension points, `{% block extra_head %}` and `{% block extra_js %}`, so individual pages can add page-specific styles or scripts without editing the shell itself.
- **`webpages/*.html`**; One template per page. Each corresponding view in `views.py` passes it context data (e.g., `product_details.html` receives a single `product` plus 4 `random_products` for "you may also like").

### Static assets (`gp/static/`)
- **`css/styles.css`**; All visual styling for the site.
- **`js/cart.js`**; Listens for clicks on any element with the `.update_cart` class (the +/− buttons), reads the `data-product` and `data-action` attributes, and sends that info to the `/update_item/` endpoint via a `fetch()` POST with the CSRF token attached. On success it reloads the page so the updated cart totals show. It also redirects unauthenticated users to the login page before attempting an update.
- **`js/index.js`**; Two small pieces of homepage UI logic: toggling the mobile hamburger nav menu open/closed, and showing a promotional popup one second after the page loads (with a close button).
- **`js/slider.js`**; Initializes the [Glide.js](https://glidejs.com/) carousel library on the homepage hero banner (`#glide_1`), configuring it as a single-item, linear-animated carousel.
- **`js/zoomsl.min.js`**; Third-party, minified plugin providing the zoom-on-hover effect for product images on the product detail page.
- **`images/`**; Category thumbnails, banners, logo, and product photos referenced by the templates and `Product.image` field.

## How It Works

**1. Routing:** A request first hits `gp/gp/urls.py`, which forwards everything to `gp/gpp/urls.py`. That file routes to either a page view (returns HTML) or, under `/api/`, to a DRF viewset (returns JSON).

**2. Browsing products:** `index`, `product`, and `product2` views pull `Product` objects from the database (`Product.objects.filter(...)`) and hand them to templates for display. `on_sale_products` are products where `discount__gt=0`.

**3. Cart:** Every logged-in user has one `Customer` profile (linked 1-to-1 with Django's `User`) and one "incomplete" `Order` at a time, which acts as their active cart. Adding a product creates/updates an `OrderItem` row linked to that order. The `updateItem` view (called via AJAX from `cart.js`) increments/decrements quantity and deletes the `OrderItem` if it hits zero. `remove_from_cart` fully removes or decrements an item from a standard (non-AJAX) link.

**4. Cart totals:** The `cart` view calculates `subtotal` (sum of price × quantity across items), a flat 5% `tax`, and `grand_total`, all computed in Python and passed to the template.

**5. Auth:** `signup_view` creates a Django `User` plus a linked `Customer` record and logs the user in immediately. `login_view` authenticates against Django's built-in auth and redirects home on success or shows an error message on failure. `logout_view` ends the session.

**6. Checkout:** The `checkout` page collects shipping details. `process_checkout` (POST-only, `@login_required`) saves a `ShippingAddress` linked to the customer's current order, marks that `Order.complete = True` (closing out the cart), and redirects to `payment_confirmation`.

**7. REST API:** `/api/products/` and `/api/categories/` are full CRUD JSON endpoints auto-generated by DRF's router; useful for a future mobile app, admin dashboard, or third-party integration without touching the website's HTML.

## Data Models

| Model | Purpose | Key Fields |
|---|---|---|
| `Customer` | Extends Django's `User` with store-specific info | `user` (1-to-1), `name`, `email` |
| `Category` | Groups products | `name`, `description` |
| `Product` | A sellable item | `name`, `description`, `price`, `category` (FK), `stock`, `image`, `discount` |
| `Order` | A customer's cart (or completed order) | `customer` (FK), `complete`, `transaction_id`, plus computed `get_cart_total` / `get_cart_items` |
| `OrderItem` | A single line item within an order | `product` (FK), `order` (FK), `quantity`, plus computed `get_total` |
| `ShippingAddress` | Delivery details for a completed order | `customer` (FK), `order` (FK), `address`, `city`, `state`, `zipcode` |

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/XanaChihiroFZ/Python-and-Django-E-commerce-Website-2.git
cd Python-and-Django-E-commerce-Website-2/gp

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install django djangorestframework

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create an admin account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` for the store, and `http://127.0.0.1:8000/admin/` for the admin panel.

**Running the test suite:** the unit and integration tests run with just `python manage.py test`. The functional test in `tests.py` additionally requires `pip install selenium` and a matching **ChromeDriver** installed and on your `PATH`, since it launches a real Chrome browser.

## Notes / Future Improvements

- `DEBUG = True` and a hardcoded `SECRET_KEY` are fine for local development but **must** be changed (via environment variables) before any real deployment.
- `ALLOWED_HOSTS` is currently empty and would need the production domain added.
- No `requirements.txt` is included in the file list above; it's recommended to add one (`pip freeze > requirements.txt`) so the exact dependency versions are reproducible.
- Payment processing is simulated (checkout marks the order complete and shows a confirmation page); no real payment gateway (e.g., Stripe/PayPal) is integrated yet.

## Acknowledgment

This project was developed as a **client commission**. It's showcased here to demonstrate full-stack Django development skills; including database design, authentication, a working shopping cart/checkout flow, and REST API design; for portfolio purposes.

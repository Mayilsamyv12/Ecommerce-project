# Eshop - Django E-commerce Project

Eshop is a fully functional e-commerce web application built with Django and Python. It provides a complete online shopping experience with features for customers to browse products, manage their cart, place orders, and track their delivery status.

## Features

*   **User Authentication:** Secure Sign Up, Login, and Logout functionality.
*   **Product Catalog:** Browse products by category or search for specific items.
*   **Product Details:** View detailed product descriptions, prices, and images.
*   **Shopping Cart:** Add items to cart, update quantities, and view total cost.
*   **Checkout Logic:** Secure checkout process with address and phone number collection.
*   **Order Management:**
    *   Place orders.
    *   View order history.
    *   Track order status (Placed, Shipped, Out For Delivery, Delivered).
*   **User Profile:** Manage profile details and change passwords.
*   **Reviews & Ratings:** Submit feedback and ratings for purchased products.
*   **Static Pages:** About Us, Contact Us, Terms & Conditions, Privacy Policy.

## Tech Stack

*   **Backend:** Python, Django 5.0.1
*   **Database:** MySQL
*   **Frontend:** HTML, CSS, JavaScript (Django Templates)
*   **Media Handling:** Pillow (for product images)

## Prerequisites

*   Python 3.x installed
*   MySQL Server installed and running

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd shopping
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content if it doesn't exist, then install:
    ```bash
    pip install django mysqlclient pillow
    ```

4.  **Database Configuration:**
    *   Create a MySQL database named `shopping`.
    *   Update the database credentials in `Eshop/settings.py` if your MySQL root password differs:
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'shopping',
                'USER': 'root',
                'PASSWORD': 'YOUR_PASSWORD', # Update this
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }
        ```

5.  **Apply Migrations:**
    Create the database tables.
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin):**
    Access the Django admin panel to manage products and orders.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the Application:**
    *   Storefront: `http://127.0.0.1:8000/`
    *   Admin Panel: `http://127.0.0.1:8000/admin/`

## Project Structure

*   `Eshop/`: Project configuration settings.
*   `store/`: Main application containing models, views, and urls for the store.
*   `templates/`: HTML templates for the UI.
*   `uploads/`: Directory for storing uploaded product images.
*   `static/`: Static files (CSS, JS, Images).

## Usage

*   **Admin:** Log in to the admin panel to add Categories and Products.
*   **Customer:** Sign up for an account to start shopping.

# Phimart - E-commerce REST API

Phimart is a modern E-commerce REST API built using Django Rest Framework (DRF).
This project provides APIs for managing products, categories, carts, orders, and user authentication using JWT.

The project also includes interactive API documentation using Swagger.

---

# Features

* Product Management API
* Category Management API
* Cart & Cart Item APIs
* Order Management API
* JWT Authentication using Djoser
* Interactive Swagger Documentation
* RESTful API Design
* Serializer Validation
* Pagination Support
* Modular App Structure

---

# Technologies Used

* Python
* Django
* Django Rest Framework (DRF)
* Djoser
* Simple JWT
* drf-yasg (Swagger Documentation)
* SQLite / PostgreSQL

---

# Project Structure

```bash
phimart/
│
├── products/
├── carts/
├── orders/
├── users/
├── categories/
├── core/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/phimart.git
cd phimart
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

Example:

```env
SECRET_KEY=your_secret_key
DEBUG=True
```

---

# Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Create Superuser

```bash
python manage.py createsuperuser
```

---

# Run Development Server

```bash
python manage.py runserver
```

Server will run at:

```bash
http://127.0.0.1:8000/
```

---

# API Endpoints

## Products

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| GET    | `/api/v1/products/`      | Get all products   |
| POST   | `/api/v1/products/`      | Create product     |
| GET    | `/api/v1/products/<id>/` | Get single product |
| PUT    | `/api/v1/products/<id>/` | Update product     |
| DELETE | `/api/v1/products/<id>/` | Delete product     |

---

## Categories

| Method | Endpoint              | Description        |
| ------ | --------------------- | ------------------ |
| GET    | `/api/v1/categories/` | Get all categories |
| POST   | `/api/v1/categories/` | Create category    |

---

## Carts

| Method | Endpoint              | Description   |
| ------ | --------------------- | ------------- |
| POST   | `/api/v1/carts/`      | Create cart   |
| GET    | `/api/v1/carts/<id>/` | Retrieve cart |
| DELETE | `/api/v1/carts/<id>/` | Delete cart   |

---

## Orders

| Method | Endpoint          | Description  |
| ------ | ----------------- | ------------ |
| GET    | `/api/v1/orders/` | List orders  |
| POST   | `/api/v1/orders/` | Create order |

---

# Authentication

JWT Authentication is implemented using **Djoser** and **Simple JWT**.

## Obtain Access Token

```http
POST /auth/jwt/create/
```

Example Request:

```json
{
    "email": "admin@example.com",
    "password": "yourpassword"
}
```

---

## Refresh Token

```http
POST /auth/jwt/refresh/
```

---

# Swagger Documentation

Swagger UI is available at:

```bash
/swagger/
```

Redoc documentation:

```bash
/redoc/
```

---

# Example API Response

```json
{
    "id": 1,
    "name": "iPhone 15",
    "price": 1200,
    "stock": 5
}
```

---

# Future Improvements

* Payment Gateway Integration
* Product Reviews & Ratings
* Search & Filtering
* Wishlist Feature
* Docker Support
* CI/CD Pipeline
* Redis Caching

---

# Testing

Run tests using:

```bash
python manage.py test
```

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

# Author

Developed by EAN.

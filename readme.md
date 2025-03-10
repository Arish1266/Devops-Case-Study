# Ipswich Electronics E-commerce

A Django-based e-commerce platform for electronics retail, featuring a responsive design and comprehensive shopping experience.

## Features

- Product catalog with filtering and sorting
- Shopping cart functionality
- Secure checkout process
- User authentication and profiles
- Admin interface for product management
- Responsive design using Bootstrap
- Category-based product organization

## Tech Stack

- Django 4.2
- Python 3.8+
- Bootstrap 5
- SQLite (Development)
- Pillow for image handling
- Django Crispy Forms
- Django AllAuth

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/django-retail-mvt-app.git
cd django-retail-mvt-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the application.

## Project Structure

```
ipswich_electronics/
├── manage.py
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
│   └── products/
├── templates/
│   ├── base.html
│   ├── products/
│   ├── cart/
│   ├── checkout/
│   └── accounts/
└── ipswich_retail/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
    └── apps/
        ├── products/
        ├── cart/
        ├── checkout/
        └── accounts/
```

## Development

### Creating New Products

1. Log in to the admin interface at http://127.0.0.1:8000/admin/
2. Navigate to Products section
3. Click "Add Product" and fill in the details

### Running Tests

```bash
python manage.py test
```

## Deployment

The application is configured for deployment on PythonAnywhere or Render.

1. Set up your hosting platform
2. Configure environment variables
3. Update settings.py with production settings
4. Collect static files:
```bash
python manage.py collectstatic
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
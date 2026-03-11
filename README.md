# set_lists
My band and I need to keep track of the hundreds of songs we know and the many set lists we write for live shows. This app is a Django website that allows us to log in, contribute to our master song list as well as create and maintain set lists.

## Prerequisites

- Python 3.8+
- pip
- (optional) virtualenv or venv

## Local setup (macOS / Linux)

1. Clone the repository and change into the project directory

    git clone <repository-url>
    cd <repository-directory>

2. Create and activate a virtual environment

    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies

    pip install -r requirements.txt

4. (Optional) Copy example environment file and set secrets

    cp .env.example .env
    # Edit .env to set SECRET_KEY, DEBUG, DATABASE settings, etc.

5. Apply migrations

    python manage.py migrate

6. Create a superuser (optional, for admin access)

    python manage.py createsuperuser

7. Run the development server

    python manage.py runserver
    # To allow external devices on your local network:
    python manage.py runserver 0.0.0.0:8000

## Useful commands

- Run tests

    python manage.py test

- Collect static files (for production)

    python manage.py collectstatic

- Load initial data fixtures (if provided)

    python manage.py loaddata <fixture-file>


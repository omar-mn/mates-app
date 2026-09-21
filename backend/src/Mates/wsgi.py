import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"Mates.settings.{os.getenv('ENV', 'dev')}")

application = get_wsgi_application()

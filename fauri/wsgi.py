import os
from django.core.wsgi import get_wsgi_application

# Основной платформой для развертывания Django является WSGI, стандарт Python для веб-серверов и приложений.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fauri.settings")

application = get_wsgi_application()

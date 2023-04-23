import os

from django.core.asgi import get_asgi_application
#ASGI обеспечивает интерфейс между асинхронными веб-серверами Python и платформами. Эта поддержка является дополнением к поддержке WSGI.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fauri.settings')

application = get_asgi_application()

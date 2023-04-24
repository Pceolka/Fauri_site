import locale
from django.apps import AppConfig


# Класс AppConfig, используемый для настройки приложения, имеет атрибут класса пути, который представляет собой
# абсолютный путь к каталогу, который Django будет использовать в качестве единого базового пути для приложения.

class StoreConfig(AppConfig):
    name = 'store'

    def ready(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU')

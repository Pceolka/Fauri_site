# Fauri_site
Сайт созданный на Django специально для клуба по спортивному ориентированию FAURI.
Инструкции по использованию в первую очередь в PyCharm:

-Запуск сервера  
 py manage.py runserver или python manage.py runserver

-Выключение сервера 
 CTRL-BREAK

-Создание суперпользователя(для админ панели) 
 python manage.py createsuperuser

-Выполнения миграций 
 python manage.py makemigrations 
 python manage.py makemigrations store
 python manage.py migrate
 
-Создания Бэкапов 
 cp ваша_база_данных.db backup.db

-Восстановите из бэкапа: 
cp backup.db ваша_база_данных.db

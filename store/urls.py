from .views import news
from django.urls import path
from django.urls import path
from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', news, name='news'),
    path("news/", views.news, name='news'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path('news/<int:id>/', views.single, name='single'),
    path('calendars/', views.calendars, name='calendars'),
]

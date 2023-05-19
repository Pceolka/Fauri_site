from .views import news
from django.urls import path
from . import views

urlpatterns = [
    path('', news, name='news'),
    path("news/", views.news, name='news'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path('news/<int:id>/', views.single, name='single'),
    path('calendars/', views.calendars, name='calendars'),
    path('gallerey/', views.gallerey, name='gallerey'),
    path('archive/', views.archive, name='archive'),
    path('pdf_detail/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
]

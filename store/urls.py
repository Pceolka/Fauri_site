from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path("news/", views.news, name='news'),
    path("about/", views.about, name='about'),
    path('category/<str:category>/', views.news_by_category, name='news_by_category'),
    path("contact/", views.contact, name='contact'),
    path('news/<int:id>/', views.single, name='single'),
    path('calendars/', views.calendars, name='calendars'),
    path('gallerey/', views.gallerey, name='gallerey'),
    path('archive/', views.archive, name='archive'),
    path('pdf_detail/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
    path('get-event-info/', views.get_event_info, name='get_event_info'),
]

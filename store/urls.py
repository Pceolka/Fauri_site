from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("news/", views.news, name='news'),
    path("index/", views.index, name='index'),
    path("about/", views.about, name='about'),
    path('category/<str:category>/', views.news_by_category, name='news_by_category'),
    path("contact/", views.contact, name='contact'),
    path('news/<int:id>/', views.single, name='single'),
    path('calendars/', views.calendars, name='calendars'),
    path('archive/', views.archive, name='archive'),
    path('search/', views.search_articles, name='search'),
    path('pdf_detail/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
    path('get-event-info/', views.get_event_info, name='get_event_info'),
]

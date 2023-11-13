from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import date
from django.shortcuts import render
import datetime
from .models import Event, Pdfs, Partners, Slider
from datetime import datetime
from django.db.models import Q
from django.db import models


# Создание видов

def news(request):
    latest_events = Event.objects.order_by('-creation_day')[:6]
    return render(request, 'news.html', {'latest_events': latest_events})


def trending(request):
    trending_texts = Trending.objects.all()
    context = {'trending_texts': trending_texts}
    return render(request, 'base.html', context)


def single(request, id):
    news = get_object_or_404(Event, id=id)
    popular_event = Event.objects.order_by('-is_popular')[:6]
    return render(request, 'single.html', {'news': news, "popular_event": popular_event})


def pdf_detail(request, pdf_id):
    pdf = get_object_or_404(Pdfs, pk=pdf_id)
    return FileResponse(open(pdf.pdfile.path, 'rb'), content_type='application/pdf')


def about(request):
    return render(request, "about.html")


def index(request):
    partners_img = Partners.objects.all()
    slider_img = Slider.objects.all()
    return render(request, "index.html", {'partners_img':partners_img, 'slider_img': slider_img})


def news_by_category(request, category):
    # Получаем список новостей для указанной категории
    news_list = Event.objects.filter(category=category).order_by('-creation_day')
    per_page = 6

    category_title = category

    paginator = Paginator(news_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем список всех категорий
    category_list = Event.objects.values_list('category', flat=True).distinct()

    context = {
        'category_list': category_list,
        'category_title': category_title,
        'news_list': news_list,
        'page_obj': page_obj,
    }

    return render(request, 'news_by_category.html', context)


def contact(request):
    return render(request, "contact.html")

def search_articles(request):
    query = request.GET.get('query', '')

    articles = Event.objects.filter(
        (models.Q(header__icontains=query) | models.Q(description__icontains=query))
    )

    context = {
        'query': query,
        'articles': articles,
    }


    return render(request, "search.html", context)


def archive(request):
    pdfs_list = Pdfs.objects.order_by('-day')



    # Фильтрация по году
    year = request.GET.get('year')
    if year:
        pdfs_list = pdfs_list.filter(day__year=int(year))

    # Фильтрация по статусу регистрации
    registration_status = request.GET.get('registration')
    if registration_status:
        if registration_status == 'open':
            pdfs_list = pdfs_list.exclude(Q(register__isnull=True) | Q(register=''))
        elif registration_status == 'closed':
            pdfs_list = pdfs_list.filter(Q(register__isnull=True) | Q(register=''))

    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        pdfs_list = pdfs_list.filter(bazeinfo__icontains=search_query)

    # Сортировка по категории
    category = request.GET.get('category')
    if category:
        pdfs_list = pdfs_list.filter(category_text=category)

    # Сортировка по организаторам
    organizers = request.GET.get('organizers')

    if organizers:
        if organizers == 'Прочее':
            pdfs_list = pdfs_list.exclude(organizers='FAURI')
            pdfs_list = pdfs_list.exclude(organizers='Galata')
            pdfs_list = pdfs_list.exclude(organizers='Tiras-Orient')
            pdfs_list = pdfs_list.exclude(organizers='FOS RM')
            pdfs_list = pdfs_list.exclude(organizers='IOF')
            # Для того чтобы сортировка по строчке "Прочее" исключало остальных организаторов, добавьте их сюда
        elif organizers:
            pdfs_list = pdfs_list.filter(organizers=organizers)

    # Сортировка по году и месяцу
    month = request.GET.get('month')
    if month:
        pdfs_list = pdfs_list.filter(day__month=int(month))

    if 'reset_filters' in request.GET:
        # Обработка сброса фильтров
        pdfs_list = Pdfs.objects.order_by('-day')

    paginator = Paginator(pdfs_list, 10)  # Set the number of items per page

    page_number = request.GET.get('page')  # Get the current page number from the request

    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page number

    context = {
        'page_obj': page_obj,
    }


    return render(request, "archive.html", context)


# Calendar
def calendars(request):

    today = date.today()
    news_all_all = Event.objects.filter(day__gte=today).exclude(category__contains='пусто').order_by('day')

    return render(request, 'calendars.html', {'news_all_all': news_all_all})


def get_closest_event():
    current_date = datetime.date.today()
    closest_event = Event.objects.filter(day__gte=current_date).order_by('day').first()
    return closest_event


def get_event_info(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.get(id=event_id)
        data = {
            'image_url': event.image.url,
            'header': event.header,
            'event_id': event.id,  # Идентификатор события
            'date': event.day.strftime("%d.%m.%Y"),  # Преобразуем дату в строку в формате "дд.мм.гггг"
            'time': event.start_time.strftime("%H:%M") if event.start_time else None,
            # Преобразуем время в строку в формате "чч:мм" или None, если время отсутствует
        }
    except Event.DoesNotExist:
        data = {}
    return JsonResponse(data)

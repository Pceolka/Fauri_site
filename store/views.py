from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import date
from django.shortcuts import render
import datetime
import calendar
from django.utils.safestring import mark_safe
from .utils import MainCalendar
from .models import Event, Pdfs
from django.utils import timezone


# Создание видов

def news(request):
    latest_events = Event.objects.order_by('-creation_day')[:6]
    return render(request, 'news.html', {'latest_events': latest_events})


def single(request, id):
    news = get_object_or_404(Event, id=id)
    return render(request, 'single.html', {'news': news})


def pdf_detail(request, pdf_id):
    pdf = get_object_or_404(Pdfs, pk=pdf_id)
    return FileResponse(open(pdf.pdfile.path, 'rb'), content_type='application/pdf')


def about(request):
    return render(request, "about.html")


def index(request):
    return render(request, "index.html")


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


def gallerey(request):
    return render(request, "gallerey.html")


# Calendar
def calendars(request):
    pdfs_list = Pdfs.objects.order_by('-creation_day')[:10]
    today = date.today()
    news_all_all = Event.objects.filter(day__gte=today).exclude(category__contains='пусто').order_by('day')

    return render(request, 'calendars.html', {'news_all_all': news_all_all, 'pdfs_list': pdfs_list})


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

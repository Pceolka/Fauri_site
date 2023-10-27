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
from django.db.models.functions import ExtractYear
from datetime import datetime

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


# def archive(request):
#    pdfs_list = Pdfs.objects.order_by('-creation_day')[:10]
 #   return render(request, "archive.html", {'pdfs_list': pdfs_list})





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
            pdfs_list = pdfs_list.filter(register='Открыта')
        elif registration_status == 'closed':
            pdfs_list = pdfs_list.exclude(register='Открыта')

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
            pdfs_list = pdfs_list.exclude(organizers='Fauri')
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

    pdfs_list = pdfs_list[:10]

    return render(request, "archive.html", {'pdfs_list': pdfs_list})

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

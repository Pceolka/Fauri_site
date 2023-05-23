from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
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


def contact(request):
    return render(request, "contact.html")


def archive(request):
    pdfs = Pdfs.objects.all()
    return render(request, 'archive.html', {'pdfs': pdfs})


def gallerey(request):
    return render(request, "gallerey.html")


# Calendar
def calendars(request):
    return render(request, 'calendars.html')


def get_event_info(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.get(id=event_id)
        # Вам нужно возвратить необходимую информацию о событии
        data = {
            'image_url': event.image.url,
            'header': event.header,
            # Дополнительная информация о событии, которую вы хотите передать
        }
    except Event.DoesNotExist:
        data = {}
    return JsonResponse(data)

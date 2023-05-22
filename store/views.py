from django.core.paginator import Paginator
from django.http import FileResponse
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
    newss = Event.objects.order_by('-creation_day')[:6]
    news_competition = Event.objects.filter(category='соревнования').order_by('-creation_day')[:3]
    news_worldcomp = Event.objects.filter(category='международные соревнования').order_by('-creation_day')[:3]
    news_event = Event.objects.filter(category='событие').order_by('-creation_day')[:3]
    news_train = Event.objects.filter(category='тренировка').order_by('-creation_day')[:4]

    return render(request, 'news.html', {'newss': newss, 'news_competition': news_competition, 'news_worldcomp': news_worldcomp, 'news_event': news_event, 'news_train': news_train})


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
def calendars(request, extra_context=None):
    after_day = request.GET.get('day__gte', None)
    extra_context = extra_context or {}

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                   day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month,
                               day=1)  # find first day of next month

    month_text = datetime.date(year=d.year, month=d.month, day=1)

    extra_context['previous_month'] = '?day__gte=' + str(previous_month)
    extra_context['next_month'] = '?day__gte=' + str(next_month)

    extra_context['year'] = str(month_text.year)
    extra_context['month'] = calendar.month_name[month_text.month]

    allevents = Event.objects.filter(day__isnull=False).filter(day__month=d.month).order_by('day')
    extra_context['allevents'] = allevents

    today = timezone.now().date()
    events = Event.objects.filter(day__isnull=False, day__month=d.month, day__gte=today).order_by('day')
    extra_context['events'] = events

    cal = MainCalendar()
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="120" height="50"')
    extra_context['calendar'] = mark_safe(html_calendar)
    return render(request, 'calendars.html', extra_context)

from store.models import Trending
from datetime import datetime, date
import datetime
import calendar
from .models import Event
from .utils import MainCalendar
from django.utils.html import mark_safe

def trending_texts(request):
    trending_text = Trending.objects.all()
    return {'trending_texts': trending_text}


def count_records(request):
    count_competition = Event.objects.filter(category='соревнования').count()
    count_worldcomp = Event.objects.filter(category='международные соревнования').count()
    count_event = Event.objects.filter(category='событие').count()
    count_train = Event.objects.filter(category='тренировка').count()

    news_all = Event.objects.order_by('-creation_day')[:4]
    news_competition = Event.objects.filter(category='соревнования').order_by('-creation_day')[:4]
    news_worldcomp = Event.objects.filter(category='международные соревнования').order_by('-creation_day')[:4]
    news_event = Event.objects.filter(category='событие').order_by('-creation_day')[:4]
    news_train = Event.objects.filter(category='тренировка').order_by('-creation_day')[:4]

    context = {'count_competition': count_competition, 'count_worldcomp': count_worldcomp, 'count_event': count_event,
               'count_train': count_train, 'news_competition': news_competition, 'news_worldcomp': news_worldcomp, 'news_event': news_event, 'news_train': news_train, 'news_all': news_all}
    return context


# Calendar




def calendar_context(request):
    after_day = request.GET.get('day__gte', None)

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)
    previous_month = previous_month - datetime.timedelta(days=1)
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month, day=1)

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])
    next_month = next_month + datetime.timedelta(days=1)
    next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)

    month_text = datetime.date(year=d.year, month=d.month, day=1)

    previous_month_link = '?day__gte=' + str(previous_month)
    next_month_link = '?day__gte=' + str(next_month)

    year = str(month_text.year)
    month = calendar.month_name[month_text.month]

    allevents = Event.objects.filter(day__isnull=False).filter(day__month=d.month).order_by('day')
    events = Event.objects.filter(day__isnull=False, day__month=d.month, day__gte=datetime.date.today()).order_by('day')

    cal = MainCalendar(events=allevents)
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td width="120" height="50"')


    return {
        'previous_month': previous_month_link,
        'next_month': next_month_link,
        'year': year,
        'month': month,
        'allevents': allevents,
        'events': events,
        'calendar': mark_safe(html_calendar)
    }



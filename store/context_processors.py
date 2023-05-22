from store.models import Trending
from .models import Event, Pdfs


def trending_texts(request):
    trending_texts = Trending.objects.all()
    return {'trending_texts': trending_texts}


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


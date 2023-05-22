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
    context = {'count_competition': count_competition, 'count_worldcomp': count_worldcomp, 'count_event': count_event,
               'count_train': count_train}
    return context


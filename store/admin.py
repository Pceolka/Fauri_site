import datetime
import calendar
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

from .models import Pdfs, Trending
from .models import Event
from .utils import EventCalendar


# регистрация моделей

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Event
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    list_display = ['header', 'day', 'start_time', 'category', 'creation_day']
    ordering = ['-creation_day']
    change_list_template = 'change_list.html'
    form = EventForm

    def changelist_view(self, request, extra_context=None):
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

        extra_context['previous_month'] = reverse('admin:store_event_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:store_event_changelist') + '?day__gte=' + str(next_month)

        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventAdmin, self).changelist_view(request, extra_context)


admin.site.register(Event, EventAdmin)


class PDFAdmin(admin.ModelAdmin):
    list_display = ['bazeinfo', 'creation_day', 'info_text', 'info_pdf', 'rezul_text', 'rezul_pdf']
    ordering = ['-creation_day']


admin.site.register(Pdfs, PDFAdmin)

admin.site.register(Trending)

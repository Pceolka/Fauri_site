from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event


class MainCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(MainCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        events_from_day = self.events.filter(day__day=day)
        events_html = '<ul >''</ul>'
        current_day = datetime.datetime.now().day

        if day == 0:
            return '<div class="calendar__number">&nbsp;</div>'  # day outside month
        else:
            if events_from_day:
                return '<div class="calendar__number calendar__number--current %s %s" data-id="%d">%d%s</div>' % (self.cssclasses[weekday], 'event', events_from_day[0].id, day, events_html)
            elif day == current_day:
                return '<div class="calendar__number %s %s">%d%s</div>' % (self.cssclasses[weekday], 'today', day, events_html)
            else:
                return '<div class="calendar__number %s">%d%s</div>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<div class="calendar__date">%s</div>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(day__month=themonth)

        v = []
        a = v.append
        a('<div class="calendar">')
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</div>')
        a('\n')
        return ''.join(v)








class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(day__month=themonth)

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

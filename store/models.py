import datetime
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


# Создание моделей

# Новости
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.TextField(u'Заголовок', help_text=u'Обязательное поле', max_length=25)
    author = models.CharField(u'Автор новости', help_text=u'Обязательное поле', max_length=25, default='fauri')
    image = models.ImageField(u'Картинка', help_text=u'Обязательное поле', upload_to='media/')
    description = models.TextField(u'Описание', default="")
    day = models.DateField(u'Дата события', blank=True, null=True)
    start_time = models.TimeField(u'Время начала события', blank=True, null=True)
    end_time = models.TimeField(u'Время конца события ', help_text=u'Хотя бы примерное)', blank=True, null=True)
    creation_day = models.DateField(u'Дата создания ', help_text=u'Обязательное поле', default=datetime.date.today)

    def __str__(self):
        return f"{self.header} ({self.day} - {self.creation_day})"

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

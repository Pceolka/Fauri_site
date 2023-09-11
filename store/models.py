import datetime
from django.db import models
from django.urls import reverse


# Создание моделей
class Trending(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(u'Заголовок', help_text=u'заголовок "Срочные новости"', default="")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Срочное'


class Pdfs(models.Model):
    id = models.AutoField(primary_key=True)
    creation_day = models.DateField(u'Дата создания ', help_text=u'Обязательное поле', default=datetime.date.today)
    bazeinfo = models.TextField(u'Первый столбик', help_text=u'время и место проведения', default="")

    info_text = models.TextField(u'Второй столбик', default="", blank=True, null=True)
    info_pdf = models.FileField(u'Второйстолб', upload_to='static/pdf_files/', help_text=u'файл', blank=True, null=True)

    rezul_text = models.TextField(u'Третий столбик', default="", blank=True, null=True)
    rezul_pdf = models.FileField(u'Третийстлб', upload_to='static/pdf_files/', help_text=u'файл', blank=True, null=True)

    def __str__(self):
        return f"{self.bazeinfo} ({self.rezul_text} - {self.creation_day})"

    class Meta:
        verbose_name = u'Архив PDF файлов'


# Новости
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.TextField(u'Заголовок', help_text=u'Обязательное поле', default="")
    author = models.CharField(u'Автор новости', help_text=u'', max_length=25, default='fauri')
    image = models.ImageField(u'Картинка', help_text=u'', upload_to='media/')
    description = models.TextField(u'Описание', default="")
    category = models.TextField(u'Категория события', default="")
    day = models.DateField(u'Дата события', blank=True, null=True)
    start_time = models.TimeField(u'Время начала события', blank=True, null=True)
    end_time = models.TimeField(u'Время конца события ', help_text=u'Хотя бы примерное)', blank=True, null=True)
    creation_day = models.DateField(u'Дата создания ', help_text=u'', default=datetime.date.today)

    def __str__(self):
        return f"{self.header} ({self.day} - {self.creation_day})"

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

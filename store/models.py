import datetime
from django.db import models
from django.urls import reverse


# Создание моделей
class Trending(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(default="")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Срочное'
        verbose_name_plural = u'Срочное'


class Pdfs(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField(u'Дата проведения', blank=True, null=True)
    bazeinfo = models.TextField(u'Название', default="")
    CATEGORY_CHOICES = [
        ('Событие', 'Событие'),
        ('Тренировка', 'Тренировка'),
        ('Международные соревнования', 'Международные соревнования'),
        ('Соревнования', 'Соревнования'),
        # Добавьте здесь все категории, которые вам нужны
    ]
    category_text = models.CharField(
        u'Категория',
        max_length=50,  # Увеличьте максимальную длину поля, если это необходимо
        choices=CATEGORY_CHOICES,
        default='событие',  # Установите категорию по умолчанию, если необходимо
    )
    organizers = models.TextField(u'Организаторы', default="", blank=True, null=True)
    register = models.TextField(u'Регистрация', help_text=u'Ссылка', blank=True, null=True)
    info_text = models.TextField(u'Бюллетень', default="", blank=True, null=True)
    rezul_text = models.TextField(u'Результаты', default="", blank=True, null=True)


    def __str__(self):
        return f"{self.bazeinfo}"

    class Meta:
        verbose_name = u'Архив'
        verbose_name_plural = u'Архив'



# для добавления нескольких пдф-файлов

class InfoFile(models.Model):
    id = models.AutoField(primary_key=True)
    pdf = models.ForeignKey(Pdfs, on_delete=models.CASCADE, related_name='info_files')
    file = models.FileField(u'Файл', upload_to='static/pdf_files/', help_text=u'файл')
    text_info = models.TextField(u'Информация', default="Информация", blank=True, null=True)

    def __str__(self):
        return f"{self.file.name} {self.text_info}"
    class Meta:
        verbose_name = u'Бюллетень'
        verbose_name_plural = u'Бюллетень'


class ResultFile(models.Model):
    id = models.AutoField(primary_key=True)
    pdf = models.ForeignKey(Pdfs, on_delete=models.CASCADE, related_name='rezul_files')
    file = models.FileField(u'Файл', upload_to='static/pdf_files/', help_text=u'файл')
    text_result = models.TextField(u'Результаты', default="Результаты", blank=True, null=True)

    def __str__(self):
        return f"{self.file.name} {self.text_result}"
    class Meta:
        verbose_name = u'Результаты'
        verbose_name_plural = u'Результаты'

# Новости
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.TextField(u'Заголовок', default="")
    author = models.CharField(u'Автор новости', help_text=u'', max_length=25, default='FAURI')
    image = models.ImageField(u'Картинка', help_text=u'', upload_to='', default='umolcanie.jpg')
    description = models.TextField(default="")

    CATEGORY_CHOICES = [
        ('событие', 'Событие'),
        ('тренировка', 'Тренировка'),
        ('международные соревнования', 'Международные соревнования'),
        ('соревнования', 'Соревнования'),
        # Добавьте здесь все категории, которые вам нужны
    ]
    category = models.CharField(
        u'Категория события',
        max_length=50,  # Увеличьте максимальную длину поля, если это необходимо
        choices=CATEGORY_CHOICES,
        default='событие',  # Установите категорию по умолчанию, если необходимо
    )

    day = models.DateField(u'Дата события', blank=True, null=True)
    start_time = models.TimeField(u'Время начала события', blank=True, null=True)
    end_time = models.TimeField(u'Время конца события ', blank=True, null=True)
    creation_day = models.DateField(u'Дата создания ', help_text=u'', default=datetime.date.today)
    is_popular = models.BooleanField(u'Популярная ', default=False)

    def __str__(self):
        return f"{self.header} ({self.day} - {self.creation_day})"

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))


class Partners(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.TextField(u'Заголовок или описание', default="")
    image = models.ImageField(u'Картинка', upload_to='partners_and_slider/')
    ssilka = models.TextField(u'Ссылка', default="")

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = u'Партнёр'
        verbose_name_plural = u'Партнёры'


class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.TextField(u'Заголовок или описание', default="")
    image = models.ImageField(u'Картинка', upload_to='partners_and_slider/')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = u'Слайдер'
        verbose_name_plural = u'Слайдер'

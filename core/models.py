from django.db import models


class TypeEvent(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'


class Tempo(models.Model):
    name = models.CharField(max_length=15, verbose_name='Название')
    priority = models.IntegerField(verbose_name='Приоритет')
    description = models.TextField(verbose_name='Подробное описание')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('priority',)
        verbose_name = 'Темп'
        verbose_name_plural = 'Темпы'


class Author(models.Model):
    nikName = models.CharField(max_length=15, verbose_name='NikName')

    def __str__(self):
        return self.nikName

    class Meta:
        ordering = ('nikName',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Complexity(models.Model):
    name = models.CharField(max_length=15, verbose_name='Название')
    priority = models.IntegerField(verbose_name='Приоритет')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('priority',)
        verbose_name = 'Сложность маршрута'
        verbose_name_plural = 'Сложности маршрута'


class Route(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    name = models.CharField(max_length=150, verbose_name='Название')
    trackFileURL = models.TextField(verbose_name='Ссылка на файл с треком')
    pointList = models.TextField(verbose_name='Нитка маршрута')
    photoURL = models.TextField(verbose_name='Ссылка на фотографию')
    length = models.IntegerField(verbose_name='Протяженность')
    asphalt = models.IntegerField(verbose_name='Асфальт')
    grader = models.IntegerField(verbose_name='Грейдер')
    soil = models.IntegerField(verbose_name='Грунт')
    jungle = models.IntegerField(verbose_name='Дебри')
    complexity = models.ForeignKey(Complexity, on_delete=models.PROTECT, verbose_name='Сложность маршрута')
    description = models.TextField(verbose_name='Подробное описание')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class Event(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Организатор')
    route = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Маршрут')
    name = models.CharField(max_length=150, verbose_name='Название')
    typeEvent = models.ForeignKey(TypeEvent, on_delete=models.PROTECT, verbose_name='Тип события')
    trackFileURL = models.TextField(verbose_name='Ссылка на файл с треком')
    pointList = models.TextField(verbose_name='Нитка маршрута')
    length = models.IntegerField(verbose_name='Протяженность')
    tempo = models.ForeignKey(Tempo, on_delete=models.PROTECT, verbose_name='Темп')
    startDateTime = models.DateTimeField(verbose_name='Дата и время старта')
    startPlace = models.TextField(verbose_name='Место старта')
    complexity = models.ForeignKey(Complexity, on_delete=models.PROTECT, verbose_name='Сложность маршрута')
    photoURL = models.TextField(default='', verbose_name='Ссылка на фотографию')
    description = models.TextField(verbose_name='Подробное описание')

    def __str__(self):
        return '{} ({})'.format(self.name, self.startDateTime.date())

    class Meta:
        ordering = ('-startDateTime',)
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Report(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    date = models.DateField(verbose_name='Дата поездки')
    name = models.CharField(max_length=150, verbose_name='Название')
    route = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Маршрут')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Событие')
    photoURL = models.TextField(verbose_name='Ссылка на фотографию')
    body = models.TextField(verbose_name='Содержимое отчета')

    def __str__(self):
        return '{} ({})'.format(self.name, self.date)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class VisitCount(models.Model):
    date = models.DateField(verbose_name='Дата')
    ip = models.IntegerField(verbose_name='ip-адрес')
    count = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.ip, self.count)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

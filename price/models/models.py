from django.db import models

# Create your models here.
from price.models.managers import DiaryManager

DATE_ACTION_ENUMS = [
    ('1D', 'DAILY'),
    ('1W', 'WEEKLY'),
    ('1M', 'MONTHLY'),
    ('3M', 'QUARTERLY'),
    ('6M', 'MID'),
    ('1Y', 'YEARLY'),
    ('1H', 'HOURLY'),
]

EMA_ENUMS = [
    ('EMA20', 'EMA20'),
    ('EMA50', 'EMA50'),
    ('EMA100', 'EMA100'),
    ('EMA200', 'EMA200'),
    ('EMA400', 'EMA400'),
]

ACTION_ENUMS = [
    (0, 'DID NOT TESTED'),  # based on threeshold
    (1, 'WICKED'),  # SİKİCİ GÜÇ
    (2, 'CLOSED DOWN'),
    (3, 'CLOSED UP'),

]

TERM_ENUMS = DATE_ACTION_ENUMS + EMA_ENUMS


class DiaryAction(models.Model):
    symbol = models.CharField(max_length=20, verbose_name='Asset Symbol')
    tarih = models.DateTimeField(auto_now_add=True, verbose_name='Action time')

    action = models.CharField(choices=ACTION_ENUMS, max_length=10)
    againts = models.CharField(choices=TERM_ENUMS, max_length=10, verbose_name='Against')
    comment = models.CharField(max_length=100, verbose_name='Comment')

    manager = DiaryManager()

    class Meta:
        db_table = 'ACTION'
        verbose_name_plural = 'Actions'


class DiaryNew(models.Model):
    symbol = models.CharField(max_length=20, verbose_name='Asset Symbol')
    tarih = models.DateTimeField(auto_now_add=True, verbose_name='New Time')

    title = models.CharField(max_length=40, verbose_name='Title')
    content = models.CharField(max_length=400, verbose_name='Content')

    class Meta:
        db_table = 'NEW'
        verbose_name_plural = 'News'


class DiaryChart(models.Model):
    symbol = models.CharField(max_length=20, verbose_name='Asset Symbol')
    chart = models.ImageField(verbose_name='Chart', upload_to='/charts/')

    class Meta:
        db_table = 'Chart'
        verbose_name_plural = 'Charts'

from django.db import models

from provider.models.managers import MakasFilter
from usrapp.models.models import CustomUser

"""
Veriler asagidaki siteden cekilecek:
http://www.ozbeyfiziki.com/mobil/data2.txt

:Ornek
{
"EURUSD":{
"title":"EURUSD",
"alis":"1,1572",
"satis":"1,1554",
"dusuk":"1,15656",
"yuksek":"1,15973"
},

"""


class Doviz(models.Model):
    kur = models.CharField(max_length=7, name='kur', verbose_name='Kur', unique=True)
    update_date = models.DateTimeField(verbose_name='Güncellenme Tarihi', name='update_date',
                                       auto_now_add=True)
    alis = models.FloatField(name='alis', verbose_name='Alış')
    satis = models.FloatField(name='satis', verbose_name='Satış')
    source = models.CharField(max_length=50, name='source', verbose_name='Veri Kaynağı', null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.kur} \n ' \
               f'Alış : {self.alis} \n' \
               f'Satış : {self.satis} '

    class Meta:
        db_table = 'DOVIZ'  # todo: degistir
        ordering = ['-update_date', '-kur']


class SarrafiyeMilyem(models.Model):
    kur = models.CharField(name='kur', verbose_name='Kur', max_length=10)

    alis = models.FloatField(name='alis', verbose_name='Alış')
    satis = models.FloatField(name='satis', verbose_name='Satış')
    updated_date = models.DateTimeField(auto_now_add=True, verbose_name='Güncellenme tarihi')
    source = models.CharField(max_length=50, name='source', verbose_name='Veri Kaynağı', null=True)

    def __str__(self):
        return f'{self.kur} Sarrafiye \n' \
               f'Zaman: {self.updated_date}\n' \
               f'Alış : {self.alis}\n' \
               f'Satış : {self.satis}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'SARRAFIYE_MILYEM'


# History Tables
class DovizH(models.Model):
    instance = models.ForeignKey(Doviz, on_delete=models.CASCADE)
    old_alis = models.FloatField(name='old_alis', verbose_name='Eski Alış')
    old_satis = models.FloatField(name='old_satis', verbose_name='Eski Satış')
    source = models.CharField(max_length=50, name='source', verbose_name='Veri Kaynağı', null=True)
    updated_date = models.DateTimeField(auto_now_add=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return f"History of {self.instance}"

    class Meta:
        db_table = 'DOVIZ_H'


class SarrafiyeMilyemH(models.Model):
    instance = models.ForeignKey(SarrafiyeMilyem, on_delete=models.CASCADE)
    old_alis = models.FloatField(name='alis', verbose_name='Eski Alış')
    old_satis = models.FloatField(name='satis', verbose_name='Eski Satış')

    update_date = models.DateTimeField(auto_now_add=True, verbose_name='Güncellenme Tarihi')
    source = models.CharField(max_length=50, name='source', verbose_name='Veri Kaynağı', null=True)

    def __str__(self):
        return f"History of {self.instance}"

    class Meta:
        db_table = 'SARRAFIYE_MILYEM_H'

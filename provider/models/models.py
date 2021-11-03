from django.db import models

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
    kur = models.CharField(max_length=7, name='kur', verbose_name='Kur')
    update_date = models.DateTimeField(verbose_name='Güncellenme Tarihi', name='update_date')
    alis = models.FloatField(name='alis', verbose_name='Alış')
    satis = models.FloatField(name='satis', verbose_name='Satış')
    dusuk = models.FloatField(name='dusuk', verbose_name='Düşük')
    yuksek = models.FloatField(name='yuksek', verbose_name='Yüksek')
    source = models.CharField(max_length=50, name='source', verbose_name='Veri Kaynağı')

    def __str__(self):
        return f'{self.kur} \n ' \
               f'Alış : {self.alis} \n' \
               f'Satış : {self.satis} '

    class Meta:
        db_table = 'OZBEY_DOVIZ'
        ordering = ['-update_date']


class Makas(models.Model):
    kur = models.OneToOneField(Doviz, on_delete=models.PROTECT)

    alis = models.FloatField(name='alis', verbose_name='Alış')
    satis = models.FloatField(name='satis', verbose_name='Satış')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.kur} MAKASLARI \n' \
               f'Zaman: {self.created_date}\n' \
               f'Alış : {self.alis}\n' \
               f'Satış : {self.satis}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'MAKAS'

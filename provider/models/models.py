from django.db import models

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
    kur = models.CharField(max_length=7, name='Kur', verbose_name='Kur')
    update_date = models.DateTimeField(verbose_name='Güncellenme Tarihi', name='Tarih',
                                       auto_now_add=True)
    alis = models.FloatField(name='Alis', verbose_name='Alış')
    satis = models.FloatField(name='Satis', verbose_name='Satış')
    dusuk = models.FloatField(name='Dusuk', verbose_name='Düşük')
    yuksek = models.FloatField(name='Yuksek', verbose_name='Yüksek')
    source = models.CharField(max_length=50, name='Veri kaynağı', verbose_name='Veri Kaynağı')

    def __str__(self):
        return f'{self.kur} \n ' \
               f'Alış : {self.alis} \n' \
               f'Satış : {self.satis} '

    class Meta:
        db_table = 'OZBEY_DOVIZ'


class Makas(models.Model):
    kur = models.OneToOneField(Doviz, on_delete=models.PROTECT)

    alis = models.FloatField(name='Alis', verbose_name='Alış')
    satis = models.FloatField(name='Satis', verbose_name='Satış')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_date} ZAMANLI {self.kur} PARITESI \n' \
               f'Alış : {self.alis} \n' \
               f'Satış : {self.satis}'

    class Meta:
        db_table = 'MAKAS'

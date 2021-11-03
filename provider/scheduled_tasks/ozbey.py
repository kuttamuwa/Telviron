import json
from datetime import datetime

from celery import shared_task
import requests

from ..models.models import Doviz

ozbey_tarih_format = '%d.%m.%Y %H:%M:%S'
ozbey_url = "http://www.ozbeyfiziki.com/mobil/data2.txt"
ozbey_tarih_parameter = 'son_guncelleme'


@shared_task()
def pull_data():
    print("Özbeyden veri çekilmeye başlanıyor...")

    # request
    response = requests.get(ozbey_url)
    data = json.loads(response.content.decode('utf-8-sig'))

    # tarih
    tarih = datetime.strptime(data[ozbey_tarih_parameter], ozbey_tarih_format)
    del data[ozbey_tarih_parameter]

    # data manipulation
    for kur, info in data.items():
        try:
            ozbey_data = Doviz(
                kur=info['title'],
                alis=float(info['alis'].replace(',', '.')),
                satis=float(info['satis'].replace(',', '.')),
                dusuk=float(info['dusuk'].replace(',', '.')),
                yuksek=float(info['yuksek'].replace(',', '.')),
                source='Ozbey',
                update_date=tarih,
            )
            ozbey_data.save()
            print(f"Kaydedildi : {ozbey_data}")
        except:  # todo: err: string indices must be integers
            if kur == ozbey_tarih_format:
                pass
            else:
                raise

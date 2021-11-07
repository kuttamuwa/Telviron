import logging

import pandas as pd
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz, SarrafiyeMilyem  # , Makas
from provider.models.serializers import DovizSerializer, SarrafiyeMilyemSerializer, \
    SarrafiyeMilyemCalculatedSerializer  # , MakasSerializer
from provider.views.paginations import StandardPagination

logger = logging.getLogger(__name__)


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [
        # IsAuthenticated
    ]
    pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['source', 'kur']
    ordering_fields = ['source', 'kur']
    ordering = 'source'

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        usr = request.user.username
        if usr == '':
            usr = 'Bilinmiyor'

        request.data['source'] = usr
        return super(DovizAPI, self).create(request, *args, **kwargs)


class SarrafiyeAPI(ModelViewSet):
    queryset = SarrafiyeMilyem.objects.all()
    serializer_class = SarrafiyeMilyemSerializer
    permission_classes = [

    ]

    # pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['kur', 'created_date', 'source']
    ordering_fields = ['kur', 'created_date', 'source']
    ordering = 'kur'

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        usr = request.user.username
        if usr == '':
            usr = 'Bilinmiyor'

        request.data['source'] = usr

        return super(SarrafiyeAPI, self).create(request, *args, **kwargs, created_by=request.user)


class HesaplananSarrafiyeAPI(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        kgrtry = Doviz.objects.get(kur__exact='KGRTRY')
        kgrtry_alis = kgrtry.alis
        kgrtry_satis = kgrtry.satis

        milyem_qset = SarrafiyeMilyem.objects.values('kur', 'alis', 'satis')

        df = pd.DataFrame(milyem_qset)
        if not df.empty:
            df.rename(columns={'alis': 'Alış', 'satis': 'Satış', 'kur': 'Kur'},
                      inplace=True)
            df['Alış'] = df['Alış'] * kgrtry_alis
            df['Satış'] = df['Satış'] * kgrtry_satis

            # to serialize
            _list = []
            for _, v in df.iterrows():
                data = {'kur': v['Kur'],
                        'alis': v['Alış'],
                        'satis': v['Satış'],
                        }
                _list.append(data)

            serializer = SarrafiyeMilyemCalculatedSerializer(_list, many=True)

            return Response(serializer.data)
        else:
            raise APIException("Veri bulunamamıştır ")

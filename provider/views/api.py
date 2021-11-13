import logging

import pandas as pd
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz, SarrafiyeMilyem, DovizH, SarrafiyeMilyemH
from provider.models.serializers import DovizSerializer, SarrafiyeMilyemSerializer, \
    SarrafiyeMilyemCalculatedSerializer, DovizHistorySerializer, SarrafiyeMilyemHistorySerializer  # , MakasSerializer
from provider.views.paginations import StandardPagination

logger = logging.getLogger(__name__)


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [
        IsAuthenticated
    ]
    # pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['source', 'kur']
    ordering = 'index'
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return Doviz.objects.all().order_by('index')

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
        IsAuthenticated
    ]

    # pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['kur', 'updated_date', 'source']
    ordering = 'index'

    def get_queryset(self):
        return SarrafiyeMilyem.objects.all().order_by('index')

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        usr = request.user.username
        if usr == '':
            usr = 'Bilinmiyor'

        request.data['source'] = usr

        return super(SarrafiyeAPI, self).create(request, *args, **kwargs)


class HesaplananSarrafiyeAPI(viewsets.ViewSet):
    permission_classes = [
        IsAuthenticated
    ]

    def list(self, request, *args, **kwargs):
        try:
            kgrtry = Doviz.objects.get(kur__exact='KGRTRY')
        except Doviz.DoesNotExist:
            raise APIException("KGRTRY tanımlanmamış ! Lütfen /doviz API'sinden tanımlayınız")

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


# HISTORY
class DovizHistoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = DovizH.objects.all()
    serializer_class = DovizHistorySerializer
    permission_classes = [
        IsAuthenticated
    ]
    renderer_classes = [
        AdminRenderer,
        JSONRenderer
    ]
    # pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter
    ]
    search_fields = ['instance', 'source']
    ordering_fields = ['updated_date', 'instance']
    ordering = ['updated_date']
    http_method_names = ['get']


class SarrafiyeHistoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = SarrafiyeMilyemH.objects.all()
    serializer_class = SarrafiyeMilyemHistorySerializer
    permission_classes = [
        IsAuthenticated
    ]
    renderer_classes = [
        AdminRenderer,
        JSONRenderer
    ]

    # pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['instance', 'source']
    ordering_fields = ['instance', 'old_alis', 'old_satis']
    ordering = 'instance'

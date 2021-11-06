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

    # def get_queryset(self):
    #     style = self.request.query_params.get('style')
    #     content_type = self.request.content_type
    #
    #     # todo: logging test
    #     logger.info('The info message')
    #     logger.warning('The warning message')
    #     logger.error('The error message')
    #
    #     # styling -> returns json
    #     # if style and content_type == 'application/json':
    #     #     qset = self._style(style)
    #     #
    #     # # default response
    #     # else:
    #     #     qset = Doviz.objects.all()
    #     #
    #     # return qset
    #     return Doviz.makas_filter.filter_ozbey()


class SarrafiyeAPI(ModelViewSet):
    queryset = SarrafiyeMilyem.objects.all()
    serializer_class = SarrafiyeMilyemSerializer
    permission_classes = [

    ]

    pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['kur', 'created_date', 'source']
    ordering_fields = ['kur', 'created_date', 'source']
    ordering = 'kur'

    def create(self, request, *args, **kwargs):
        return super(SarrafiyeAPI, self).create(request, *args, **kwargs, created_by=request.user)


class CalculatedSarrafiyeAPI(viewsets.ViewSet):
    queryset = Doviz.objects.all()

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
                # new = v.iloc[0]
                # old = v.iloc[1]

                data = {'kur': v['Kur'],
                        'alis': v['Alış'],  # 'Eski Satış': old['Satış'],
                        'satis': v['Satış'],  # 'Yeni Satış': new['Satış'],
                        }
                _list.append(data)

            serializer = SarrafiyeMilyemCalculatedSerializer(_list, many=True)

            return Response(serializer.data)
        else:
            raise APIException("Veri bulunamamıştır ")
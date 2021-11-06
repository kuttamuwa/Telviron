import logging

from rest_framework import filters
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz  # , Makas
from provider.models.serializers import DovizSerializer  # , MakasSerializer
from provider.views.paginations import StandardPagination

logger = logging.getLogger(__name__)


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [

    ]
    pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['source', 'kur']
    ordering_fields = ['source', 'kur']
    ordering = 'source'

    def get_queryset(self):
        style = self.request.query_params.get('style')
        content_type = self.request.content_type

        # todo: logging test
        logger.info('The info message')
        logger.warning('The warning message')
        logger.error('The error message')

        # styling -> returns json
        # if style and content_type == 'application/json':
        #     qset = self._style(style)
        #
        # # default response
        # else:
        #     qset = Doviz.objects.all()
        #
        # return qset
        return Doviz.makas_filter.filter_ozbey()

    def retrieve(self, request, *args, **kwargs):
        return super(DovizAPI, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        data = super(DovizAPI, self).list(request, *args, **kwargs)
        return data


# class MakasAPI(ModelViewSet):
#     queryset = Makas.objects.all()
#     serializer_class = MakasSerializer
#     permission_classes = [
#
#     ]
#
#     pagination_class = StandardPagination
#     filter_backends = [
#         filters.SearchFilter
#     ]
#     search_fields = ['kur', 'created_date', 'created_by']
#     ordering_fields = ['kur', 'created_date', 'created_by']
#     ordering = 'kur'
#
#     def create(self, request, *args, **kwargs):
#         return super(MakasAPI, self).create(request, *args, **kwargs, created_by=request.user)

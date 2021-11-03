import logging

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz, Makas
from provider.models.serializers import DovizSerializer, MakasSerializer
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

    @staticmethod
    def standard_filter(qset):
        """
        Applies standard filter on response as json
        :param qset: Doviz.objects.all()
        :return:
        """
        return qset

    def get_queryset(self):
        qset = Doviz.objects.all()
        param_filter = self.request.query_params.get('filter')

        logger.info('The info message')
        logger.warning('The warning message')
        logger.error('The error message')

        # filtering
        if param_filter:
            qset = self.standard_filter(qset)

        return qset


class MakasAPI(ModelViewSet):
    queryset = Makas.objects.all()
    serializer_class = MakasSerializer
    permission_classes = [

    ]

    pagination_class = StandardPagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['kur', 'created_date', 'created_by']
    ordering_fields = ['kur', 'created_date', 'created_by']
    ordering = 'kur'
    
    def create(self, request, *args, **kwargs):
        return super(MakasAPI, self).create(request, *args, **kwargs, created_by=request.user)
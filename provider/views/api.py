from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz, Makas
from provider.models.serializers import DovizSerializer, MakasSerializer


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [

    ]

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

        # filtering
        if param_filter:
            qset = self.standard_filter(qset)

        return qset


class MakasAPI(ModelViewSet):
    queryset = Makas.objects.all()
    serializer_class = MakasSerializer
    permission_classes = [

    ]

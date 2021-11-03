from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz, Makas
from provider.models.serializers import DovizSerializer, MakasSerializer


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [

    ]


class MakasAPI(ModelViewSet):
    queryset = Makas.objects.all()
    serializer_class = MakasSerializer
    permission_classes = [

    ]
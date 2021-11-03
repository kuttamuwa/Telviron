from rest_framework.viewsets import ModelViewSet

from provider.models.models import Doviz
from provider.models.serializers import DovizSerializer


class DovizAPI(ModelViewSet):
    queryset = Doviz.objects.all()
    serializer_class = DovizSerializer
    permission_classes = [

    ]

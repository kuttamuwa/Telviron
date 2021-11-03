from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from usrapp.models.serializers import UserSerializer, GroupSerializer, UserSerializerWithToken


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UsersAPI(APIView):
    permission_classes = [
        permissions.AllowAny,
        permissions.IsAdminUser
    ]


class GroupAPI(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]

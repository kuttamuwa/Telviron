from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from usrapp.models.serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def send_sms(request):
    if request.user:
        print("")


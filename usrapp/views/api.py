from django.contrib.auth.models import Group
from phone_verify.api import VerificationViewSet
from rest_framework import viewsets, permissions, status, response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from usrapp.models.serializers import UserSerializer, GroupSerializer, DumanSMSVerificationSerializer, DumanPhoneSerializer
from usrapp.sms_service.service import send_security_code_and_generate_session_token


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


class DumanVerificationViewSet(VerificationViewSet):
    # serializer_class = DumanSMSVerificationSerializer

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        serializer_class=DumanPhoneSerializer,
    )
    def register(self, request):
        serializer = DumanPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_token = send_security_code_and_generate_session_token(
            str(serializer.validated_data["phone_number"])
        )
        return Response({"session_token": session_token})

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        serializer_class=DumanSMSVerificationSerializer,
    )
    def verify(self, request):
        serializer = DumanSMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Security code is valid."})

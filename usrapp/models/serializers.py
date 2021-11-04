from django.contrib.auth.models import Group
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .fields import DumanPhoneNumberField
from .models import CustomUser
from ..sms_service import get_sms_backend
from ..sms_service.service import DumanPhoneVerificationService


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class DumanPhoneSerializer(serializers.Serializer):
    phone_number = DumanPhoneNumberField()


class DumanSMSVerificationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    session_token = serializers.CharField(required=True)
    security_code = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs.get("phone_number", None)
        security_code, session_token = (
            attrs.get("security_code", None),
            attrs.get("session_token", None),
        )
        # backend = get_sms_backend(phone_number=phone_number)
        backend = DumanPhoneVerificationService.backend
        verification, token_validatation = backend.validate_security_code(
            security_code=security_code,
            phone_number=phone_number,
            session_token=session_token,
        )

        if verification is None:
            raise serializers.ValidationError("Security code is not valid")
        elif token_validatation == backend.SESSION_TOKEN_INVALID:
            raise serializers.ValidationError("Session Token mis-match")
        elif token_validatation == backend.SECURITY_CODE_EXPIRED:
            raise serializers.ValidationError("Security code has expired")
        elif token_validatation == backend.SECURITY_CODE_VERIFIED:
            raise serializers.ValidationError("Security code is already verified")

        return attrs

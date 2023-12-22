from rest_framework import serializers
from .models import UsersModel


class UserSoliqSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = '__all__'
class UserLoginSerializer(serializers.Serializer):
    PS_seriya = serializers.CharField(max_length=2)
    PS_raqam = serializers.CharField(max_length=7)
    name = serializers.CharField(max_length=255)

from rest_framework import serializers
from .models import UserCard
from CheckSoliq import models


class PaymentSoliqSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = '__all__'
class AddMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = ['card_number','money']
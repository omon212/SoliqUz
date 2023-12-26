from django.shortcuts import render
from rest_framework import status


from .models import UserCard
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from PaymentSoliq.serializers import PaymentSoliqSerializer,AddMoneySerializer
from drf_yasg.utils import swagger_auto_schema

class AddCard(APIView):
    serializer_class = PaymentSoliqSerializer
    queryset = UserCard.objects.all()
    @swagger_auto_schema(request_body=PaymentSoliqSerializer)
    def post(self,request):
        serializer = PaymentSoliqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Card Added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import UpdateAPIView

class AddMoney(UpdateAPIView):
    serializer_class = AddMoneySerializer
    queryset = UserCard.objects.all()

    @swagger_auto_schema(request_body=AddMoneySerializer)
    def put(self, request, *args, **kwargs):
        pul_yuborilgan_karta = request.data.get('card_number')
        money = request.data.get('money')

        try:
            carta = UserCard.objects.get(card_number=pul_yuborilgan_karta)
        except UserCard.DoesNotExist:
            return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)




        oldingi_pul = carta.money
        hamme_pul = oldingi_pul + money
        carta.money = hamme_pul
        carta.save()

        return Response({'message': 'Money added'}, status=status.HTTP_200_OK)







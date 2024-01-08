from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse
from .models import UserCard
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response

from PaymentSoliq.serializers import PaymentSoliqSerializer, AddMoneySerializer, CheckSerializer, CheckModel
from drf_yasg.utils import swagger_auto_schema


class AddCard(APIView):
    serializer_class = PaymentSoliqSerializer
    queryset = UserCard.objects.all()

    @swagger_auto_schema(request_body=PaymentSoliqSerializer)
    def post(self, request):
        serializer = PaymentSoliqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Card Added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


import random
import datetime
import qrcode
from fpdf import FPDF

from django.shortcuts import get_object_or_404
class PayMoneyWithCheck(APIView):
    queryset = CheckModel.objects.all()
    serializer_class = CheckSerializer

    @swagger_auto_schema(request_body=CheckSerializer)
    def post(self, request):
        odam = request.data.get('name')
        pul = request.data.get("money")
        qayerga = request.data.get("where")
        fiskal_raqam = ''
        for i in range(14):
            fiskal_raqam += str(random.randint(0, 9))

        llist_series = ["UZ", "VG", "NA", "ZZ", "EP", "EZ", "LG", "ET"]
        fiskal_seriya = random.choice(llist_series)
        from UserSoliq.models import UsersModel
        # Retrieve UsersModel instance
        user_instance = get_object_or_404(UsersModel, pk=odam)

        # Create CheckModel instance with the retrieved UsersModel instance
        saver = CheckModel.objects.create(
            name=user_instance,
            money=pul,
            where=qayerga,
            fiskal_raqam=fiskal_raqam,
            fiskal_seriya=fiskal_seriya
        )
        saver.save()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # pdf.cell(200, 10, txt="Fiksal ID: " + fiksal_id, ln=1, align="C")
        pdf.cell(200, 10, txt="Fiksal Belgi: " +
                              str(fiskal_raqam), ln=1, align="C")
        pdf.cell(200, 10, txt="Fiksal Seriya: " +
                              str(fiskal_seriya), ln=1, align="C")
        pdf.cell(200, 10, txt="User: " + str(odam), ln=1, align="C")
        pdf.cell(200, 10, txt="Where: " + str(qayerga), ln=1, align="C")
        pdf.cell(200, 10, txt="Total: " + str(pul), ln=1, align="C")
        x = datetime.datetime.now()
        pdf.cell(200, 10, txt="Time: " + str(x), ln=1, align="C")

        img = qrcode.make(f"http://164.92.101.201:8000/pay/cashback/{fiskal_seriya}")
        img.save(f"uploads/check{fiskal_seriya}.png")
        # save in pdf
        pdf.image(f"uploads/check{fiskal_seriya}.png", x=80 - 10, y=80, w=80)
        pdf.output(f"uploads/check{fiskal_seriya}.pdf")
        pdf_path = f"uploads/check{fiskal_seriya}.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="uploads/check{fiskal_seriya}.pdf"'

        # ... rest of your code

        return Response({"message": "success"}, status=status.HTTP_201_CREATED)

# class PayMoneyWithCheck(APIView):
#     queryset = CheckModel.objects.all()
#     serializer_class = CheckSerializer
#     @swagger_auto_schema(request_body=CheckSerializer)
#     def post(self, request):
#         odam = request.data.get('name')
#         pul = request.data.get("money")
#         qayerga = request.data.get("where")
#         fiskal_raqam = ''
#         for i in range(14):
#             fiskal_raqam += str(random.randint(0, 9))
#
#         llist_series = ["UZ", "VG", "NA", "ZZ", "EP", "EZ", "LG", "ET"]
#         fiskal_seriya = random.choice(llist_series)
#         saver = CheckModel.objects.create(name=int(odam),money=pul,where=qayerga,fiskal_raqam=fiskal_raqam,fiskal_seriya=fiskal_seriya)
#         saver.save()
#
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)
#         # pdf.cell(200, 10, txt="Fiksal ID: " + fiksal_id, ln=1, align="C")
#         pdf.cell(200, 10, txt="Fiksal Belgi: " +
#                               str(fiskal_raqam), ln=1, align="C")
#         pdf.cell(200, 10, txt="Fiksal Seriya: " +
#                               str(fiskal_seriya), ln=1, align="C")
#         pdf.cell(200, 10, txt="User: " + str(odam), ln=1, align="C")
#         pdf.cell(200, 10, txt="Where: " + str(qayerga), ln=1, align="C")
#         pdf.cell(200, 10, txt="Total: " + str(pul), ln=1, align="C")
#         x = datetime.datetime.now()
#         pdf.cell(200, 10, txt="Time: " + str(x), ln=1, align="C")
#
#         img = qrcode.make(f"http://164.92.101.201:8000/pay/cashback/{fiskal_seriya}")
#         img.save(f"uploads/check{fiskal_seriya}.png")
#         # save in pdf
#         pdf.image(f"uploads/check{fiskal_seriya}.png", x=80 - 10, y=80, w=80)
#         pdf.output(f"uploads/check{fiskal_seriya}.pdf")
#         pdf_path = f"uploads/check{fiskal_seriya}.pdf"
#         with open(pdf_path, 'rb') as pdf_file:
#             response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="uploads/check{fiskal_seriya}.pdf"'
#
#         return Response({"message":"success"},status=status.HTTP_201_CREATED)
#
#



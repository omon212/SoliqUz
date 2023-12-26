from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSoliqSerializer, UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import UsersModel

class UserSoliqView(APIView):
    @swagger_auto_schema(request_body=UserSoliqSerializer)
    def post(self, request):
        # return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        serializer = UserSoliqSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generating access token
            access_token = AccessToken.for_user(user)

            return Response({'register': 'success', 'access_token': str(access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message: ": "error"}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def get(self, request, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Rest of your code
        access_token = str(refresh.access_token)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)

class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            ps_seriya = serializer.validated_data['PS_seriya']
            ps_raqam = serializer.validated_data['PS_raqam']
            name = serializer.validated_data['name']

            # Check if the user with provided credentials exists
            try:
                user = UsersModel.objects.get(PS_seriya=ps_seriya, PS_raqam=ps_raqam, name=name)
            except UsersModel.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            # Generate token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

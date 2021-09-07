from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serialisers import (UserSignupSerializer, UserGetTokenSerializer,
                          UserSerializer)


class APIUserSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserGetToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            if request.data['confirmation_code'] == user.confirmation_code:
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                data = {
                    "token": token
                }
                return Response(data=data, status=status.HTTP_200_OK)
            raise serializers.ValidationError({
                'confirmation_code': 'Неверный код подтверждения'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

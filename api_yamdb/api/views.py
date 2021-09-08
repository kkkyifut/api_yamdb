from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAuthorOrReadOnly, IsAdminOrSuperuserOnly
from .serialisers import (UserSignupSerializer, UserGetTokenSerializer,
                          UserSerializer, UserMeSerializer, ReviewSerializer,
                          CommentSerializer)
from users.models import User
from reviews.models import Review, Comment, Title


class APIUserSignup(APIView):

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserGetToken(APIView):

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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperuserOnly,)


class UpdateRetrieveViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class UserMeViewSet(UpdateRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

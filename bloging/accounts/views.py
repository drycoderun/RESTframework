from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from article.permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import UserSerializer
# Create your views here.

User = get_user_model()

class UserCreateAPIView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
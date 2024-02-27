from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from apps.models import User
from apps.serializers import UserModelSerializer, UserCreateModelSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ['username', 'email']


class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer

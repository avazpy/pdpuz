from rest_framework.viewsets import ModelViewSet

from apps.models import User
from apps.serializers import UserModelSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

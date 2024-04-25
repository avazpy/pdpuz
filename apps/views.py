from django_user_agents.utils import get_user_agent
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import User, UserCourse, Module, Lesson, Task, Device
from apps.serializers import UpdateUserSerializer
from apps.serializers import UserModelSerializer, UserCreateModelSerializer, UserCourseModelSerializer, \
    ModuleModelSerializer, \
    LessonModelSerializer, TaskModelSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['phone_number', 'password']
        )
    )
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = User.objects.filter(username=phone_number).first()

        if user and user.check_password(password):
            # token, created = Token.objects.get_or_create(user=user)
            token, created = Token.objects.get_or_create(user=user)

            # Get user agent data
            user_agent = get_user_agent(request)
            title = f"{user_agent.os.family}, {user_agent.browser.family}, {user_agent.browser.version_string}, {'Mobile' if user_agent.is_mobile else 'Desktop'}"

            device, created = Device.objects.get_or_create(user_id=user.id, title=title)

            return Response({"message": f"{user.username} you have logged in successfully!"},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter = (OrderingFilter, SearchFilter)
    search_fields = ('username', 'email')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    @action(detail=False, methods=['GET'], url_path='get-me')
    def get_me(self, request, pk=None):
        if request.user.is_authenticated:
            return Response({'message': f'{request.user.username}'})
        return Response({'message': f'login closed'})


class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer


class UserCourseListAPIView(ListAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseModelSerializer
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleModelSerializer
    pagination_class = None


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    pagination_class = None


class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    pagination_class = None


class UpdateUser(RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None

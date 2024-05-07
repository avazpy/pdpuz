from django_user_agents.utils import get_user_agent
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveDestroyAPIView, UpdateAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from apps.models import (Course, DeletedUser, Device, Lesson, Module, Task,
                         User, UserCourse, UserLesson, UserModule, UserTask)
from apps.serializers import (CheckPhoneModelSerializer,
                              CourseModuleModelSerializer,
                              CoursesModelSerializer, DeletedUserSerializer,
                              DeviceModelSerializer, LessonModelSerializer,
                              ModuleLessonModelSerializer,
                              ModuleModelSerializer, RegisterModelSerializer,
                              TaskModelSerializer,
                              UpdatePasswordUserSerializer,
                              UpdateUserSerializer, UserCourseModelSerializer,
                              UserModelSerializer, UserTaskModelSerializer)


class LoginView(APIView):
    permission_classes = [AllowAny, IsAuthenticated]

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

        user = User.objects.filter(phone_number=phone_number).first()

        if user and user.check_password(password):
            # token, created = Token.objects.get_or_create(user=user)
            token, created = Token.objects.get_or_create(user=user)

            # Get user agent data
            user_agent = get_user_agent(request)
            title = f"{user_agent.os.family}, {user_agent.browser.family}, {user_agent.browser.version_string}, {'Mobile' if user_agent.is_mobile else 'Desktop'}"

            device, created = Device.objects.get_or_create(user_id=user.id)  # ,title=title)

            return Response({"message": f"{user.phone_number} you have logged in successfully!"},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter = (OrderingFilter, SearchFilter)
    search_fields = ('phone_number',)
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='get-me')
    def get_me(self, request):
        if request.user.is_authenticated:
            return Response({'message': f'{request.user.phone_number}'})
        return Response({'message': f'login closed'})


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer
    pagination_class = None


class UserCourseListAPIView(ListAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CourseModuleListAPIView(ListAPIView):
    queryset = UserModule.objects.all()
    serializer_class = CourseModuleModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ModuleViewSet(ViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleLessonModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @action(['GET'], detail=True)
    def module(self, request, pk=None):
        modules = Module.objects.filter(course_id=pk)
        return Response(ModuleModelSerializer(modules, many=True).data)


class ModuleLessonListAPIView(ListAPIView):
    queryset = UserLesson.objects.all()
    serializer_class = ModuleLessonModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserTaskListAPIView(ListAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UpdateUser(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class UpdateUserPassword(UpdateAPIView):
    serializer_class = UpdatePasswordUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None
    http_method_names = ['patch']


class DeviceModelListAPIView(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceModelSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None


class CheckPhoneAPIView(GenericViewSet):
    serializer_class = CheckPhoneModelSerializer

    def list(self, request):
        phone = request.data.get('phone_number')
        response = User.objects.filter(phone_number=phone).exists()
        return Response(response)


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursesModelSerializer
    pagination_class = None

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class DeleteUserAPIView(RetrieveDestroyAPIView):
    serializer_class = DeletedUserSerializer
    queryset = DeletedUser.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        print(request.user.username, request.user.phone_number)
        DeletedUser(username=request.user.username, phone_number=request.user.phone_number).save()
        return super().delete(request, *args, **kwargs)

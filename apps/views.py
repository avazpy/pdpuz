from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveDestroyAPIView, UpdateAPIView,)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from apps.models import (Course, DeletedUser, Device, Lesson, Module, User,
                         UserLesson, UserModule, UserTask,)
from apps.serializers import (CheckPhoneModelSerializer, CourseModelSerializer,
                              DeletedUserSerializer, DeviceModelSerializer,
                              LessonModelSerializer,
                              ModuleLessonModelSerializer,
                              ModuleModelSerializer, RegisterModelSerializer,
                              UpdatePasswordUserSerializer,
                              UpdateUserSerializer, UserModelSerializer,
                              UserModuleModelSerializer,
                              UserTaskModelSerializer,)


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

class CourseAllListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer

class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserCourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(usercourse__user=self.request.user)


class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserModuleListAPIView(ListAPIView):
    queryset = UserModule.objects.all()
    serializer_class = UserModuleModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ModuleViewSet(ViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleLessonModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    @action(['GET'], detail=True)
    def module(self, request, pk=None):
        modules = Module.objects.filter(course_id=pk)
        return Response(ModuleModelSerializer(modules, many=True).data)


class ModuleLessonListAPIView(ListAPIView):
    queryset = UserLesson.objects.all()
    serializer_class = ModuleLessonModelSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserTaskListAPIView(ListAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskModelSerializer
    permission_classes = [IsAuthenticated, ]
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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('device_type', 'device_model', 'title')
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_object(self):
        return self.request.user


class CheckPhoneAPIView(GenericViewSet):
    serializer_class = CheckPhoneModelSerializer

    def list(self, request):
        phone = request.data.get('phone_number')
        response = User.objects.filter(phone_number=phone).exists()
        return Response(response)


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    pagination_class = None

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class DeleteUserAPIView(RetrieveDestroyAPIView):
    serializer_class = DeletedUserSerializer
    queryset = DeletedUser.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete', ]
    pagination_class = None

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        DeletedUser(username=request.user.username, phone_number=request.user.phone_number).save()
        return super().delete(request, *args, **kwargs)

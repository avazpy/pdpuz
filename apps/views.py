from django_filters.rest_framework import DjangoFilterBackend
from durin.views import LoginView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     UpdateAPIView, )
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import (Course, DeletedUser, Device, Lesson, Module, Task,
                         User, UserLesson, UserModule, Video, )
from apps.permissions import IsJoinedCoursePermission
from apps.serializers import (CheckPhoneModelSerializer, CourseModelSerializer,
                              DeletedUserSerializer, DeviceModelSerializer,
                              LessonDetailModelSerializer,
                              LessonModelSerializer,
                              ModuleLessonModelSerializer,
                              ModuleModelSerializer, ModuleTeacherSerializer,
                              RegisterModelSerializer, TaskModelSerializer,
                              TeacherSerializer, UpdatePasswordUserSerializer,
                              UpdateUserSerializer,
                              UserCourseTeacherModelSerializer,
                              UserModuleModelSerializer,
                              CustomAuthTokenSerializer, MyUserModelSerializer, UserModelSerializer,
                              VideoModelSerializer, LessonCRUDSerializer, ModuleCRUDSerializer, TaskGRUDSerializer,
                              CourseCRUDSerializer, VideoGRUDSerializer)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     pass
# def post(self, request, *args, **kwargs) -> Response:
#     serializer = TokenObtainPairSerializer(data=request.data)
#     response = super().post(request, *args, **kwargs)
#     if serializer.is_valid():
#         user = serializer.data.serializer.user
#         # Old tokenlarni o'chirish
#         # AuthToken.objects.filter(user=user).delete()
#         # Yangi token yaratish
#         token = AuthToken.objects.create(user=user)
#         response.data['user'] = {
#             'user': user.id,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'phone': user.phone_number
#         }
#         response.data['durin_token'] = token.token
#     return response

class TeacherAPIView(ListAPIView):
    queryset = User.objects.filter(type='teacher')
    serializer_class = TeacherSerializer
    pagination_class = None


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter = (OrderingFilter, SearchFilter)
    search_fields = ('phone_number',)
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['GET'], url_path='get-me')
    def get_me(self, request):
        if request.user.is_authenticated:
            return Response({'message': f'{request.user.phone_number}'})
        return Response({'message': f'login closed'})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        response = super().post(request, *args, **kwargs)
        if serializer.is_valid():
            user = serializer.data.serializer.user
            response.data['user'] = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone_number,
            }
        return response


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

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

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


class UserCourseTeacherListAPIView(ListAPIView):
    queryset = UserModule.objects.all()
    serializer_class = UserCourseTeacherModelSerializer
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


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsJoinedCoursePermission]
    serializer_class = LessonDetailModelSerializer


class ModuleViewSet(ViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleLessonModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    @action(['GET'], detail=True)
    def module(self, request, pk=None):
        modules = Module.objects.filter(course_id=pk)
        return Response(ModuleModelSerializer(modules, many=True).data)


class CourseAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleTeacherSerializer
    pagination_class = None

    # @action(['GET'], detail=True)
    # def module(self, request, pk=None):
    #     modules = Module.objects.filter(course_id=pk)
    #     return Response(ModelSerializer(modules, many=True).data)


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


class UserTaskRetrieveAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'lesson_id'

    def list(self, request, *args, **kwargs):
        lesson_id = self.kwargs.get(self.lookup_url_kwarg)
        if not UserLesson.objects.filter(user=self.request.user, lesson_id=lesson_id).exists():
            return Response({'msg': 'Bu lessonga access yoq', }, status=status.HTTP_403_FORBIDDEN)
        qs = Task.objects.filter(lesson_id=lesson_id, must_complete=False)
        # qs = Task.objects.filter(lesson_id=lesson_id)
        # .annotate(
        #     is_open=Case(
        #         When(Q('usertask__finished'), then=True),
        #         default=False,
        #         output_field=BooleanField()
        #     )
        # )
        return Response(TaskModelSerializer(qs, many=True).data)

        # all_task_ids = set(Task.objects.filter(lesson_id=lesson_id).values_list('id', flat=True))
        # completed_task_ids = set(
        #     UserTask.objects.filter(
        #         user=request.user, task__lesson_id=lesson_id, finished=True
        #     ).values_list('task_id', flat=True))
        # response = {
        #     'unfinished_tasks': all_task_ids.difference(completed_task_ids)
        # }
        # return Response(response)

    # def get(self, request, *args, **kwargs):
    #     user = self.request.user.id
    #     # completed = UserTask.objects.filter(user=user)
    #     if UserTask.objects.filter(user=user, task__must_complete=True):
    #         # print(super().get_queryset().filter(user=self.request.user) and UserTask.objects.filter(task__must_complete=True ))
    #         UserTask.objects.filter(user=user, finished=True).update()
    #         # return super().get_queryset()


class TaskCorrectAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None


class UpdateUser(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
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

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DeviceModelListAPIView(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceModelSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('device_type', 'device_model', 'title')
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user


class MyUserModelAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MyUserModelSerializer
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


class CustomDurinLoginAPIView(LoginView):

    @staticmethod
    def validate_and_return_user(request):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user"]


class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class LessonModelViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ModuleModulViewSet(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None

    # @action(['GET'], detail=True)
    # def module(self, request, pk=None):
    #     modules = Module.objects.filter(course_id=pk)
    #     return Response(ModuleModelSerializer(modules, many=True).data)


class TaskModulViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskGRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None


class VideoModulViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoGRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None

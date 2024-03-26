# import user_agents
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import User, UserCourse, Module, Lesson, Task

from apps.serializers import UpdateUserSerializer
from apps.serializers import UserModelSerializer, UserCreateModelSerializer, UserCourseModelSerializer, \
    ModuleModelSerializer, \
    LessonModelSerializer, TaskModelSerializer


# views.py


# class LoginView(APIView):
# @method_decorator(csrf_exempt)
# def post(self, request):
#     user_agent_str = request.headers.get('User-Agent')

# user_agent = user_agents.parse(user_agent_str)
# operating_system = user_agent.os.family
# browser_name = user_agent.browser.family
# browser_version = user_agent.browser.version_string
# device_type = 'Mobile' if user_agent.is_mobile else 'Desktop'

# print(f"Operating System: {operating_system}")
# print(f"Browser Name: {browser_name}")
# print(f"Browser Version: {browser_version}")
# print(f"Device Type: {device_type}")

# Login ni Logikasi

# return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter = (OrderingFilter, SearchFilter)
    search_fields = ('username', 'email')

    @action(detail=False, methods=['GET'], url_path='get-me')
    def get_me(self, request):
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


class UpdateUser(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = UserProfile.objects.all()
    pagination_class = None

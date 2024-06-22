from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.views import (CheckPhoneAPIView, CourseAllListAPIView,
                        CustomTokenObtainPairView,
                        DeleteUserAPIView, DeviceModelListAPIView,
                        LessonRetrieveAPIView, CourseModelViewSet,
                        TeacherAPIView, UpdateUser, ModuleModulViewSet,
                        UpdateUserPassword, UserCourseListAPIView, TaskModulViewSet,
                        UserCourseTeacherListAPIView, UserCreateAPIView, VideoModulViewSet,
                        UserModuleListAPIView, UserTaskRetrieveAPIView,
                        CustomDurinLoginAPIView, MyUserModelAPIView, UserViewSet, LessonModelViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('course', CourseModelViewSet, basename='module')
router.register('module', ModuleModulViewSet, basename='module')
router.register('lesson', LessonModelViewSet, basename='lesson')
router.register('task', TaskModulViewSet, basename='task')
router.register('video', VideoModulViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
    path('durin/login/', CustomDurinLoginAPIView.as_view(), name='durin_login'),
    path('check/phone/', CheckPhoneAPIView.as_view({'post': 'list'}), name='check_phone'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('course/', CourseAllListAPIView.as_view(), name='course_list'),
    path('user/device/', DeviceModelListAPIView.as_view(), name='device_model_list'),
    path('user/register/', UserCreateAPIView.as_view(), name='token_obtain_pair'),
    path('user/delete/', DeleteUserAPIView.as_view(), name='deleted_user'),
    path('user/my-courses/', UserCourseListAPIView.as_view(), name='user_course'),
    path('user/task/<uuid:lesson_id>', UserTaskRetrieveAPIView.as_view(), name='user_task'),
    path('user/profile/', UpdateUser.as_view(), name='user_profile_update'),
    path('user/profile/password/', UpdateUserPassword.as_view(), name='user_profile_update'),
    path('user/module/', UserModuleListAPIView.as_view(), name='course_module'),
    path('course/module/<uuid:pk>/', UserCourseTeacherListAPIView.as_view(), name='course_module_teacher'),
    path('lesson/<uuid:pk>/', LessonRetrieveAPIView.as_view(), name='module_lesson'),
    # path('task/correct/<str:pk>',TaskCorrectAPIView.as_view(), name='task_correct'),
    path('teachers/', TeacherAPIView.as_view(), name='teachers'),
    path('user/get-me', MyUserModelAPIView.as_view(), name='user_get_me'),
]

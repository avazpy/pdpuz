from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.views import CourseModuleListAPIView, ModuleLessonListAPIView, DeleteUserAPIView, UpdateUserPassword
from apps.views import UpdateUser
from apps.views import UserViewSet, UserCreateAPIView, UserCourseListAPIView, TaskListAPIView, LoginView, \
    DeviceModelListAPIView, CheckPhoneAPIView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('check/phone/', CheckPhoneAPIView.as_view({'post': 'list'}), name='check_phone'),
    path('user/device/', DeviceModelListAPIView.as_view(), name='device-model-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/register/', UserCreateAPIView.as_view(), name='token_obtain_pair'),
    path('user/login', LoginView.as_view(), name='token_login'),
    path('user/delete', DeleteUserAPIView.as_view(), name='deleted_user'),
    path('user/course/', UserCourseListAPIView.as_view(), name='user_course'),
    path('course/module/', CourseModuleListAPIView.as_view(), name='course_module'),
    path('module/lesson/', ModuleLessonListAPIView.as_view(), name='lesson'),
    path('lesson/task/', TaskListAPIView.as_view(), name='task'),
    path('user/profile/update/', UpdateUser.as_view(), name='user_profile_update'),
    path('user/profile/update/password/', UpdateUserPassword.as_view(), name='user_profile_update'),
]

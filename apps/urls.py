from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from apps.views import (CheckPhoneAPIView, CourseModuleListAPIView,
                        DeleteUserAPIView, DeviceModelListAPIView, LoginView,
                        ModuleLessonListAPIView, UpdateUser,
                        UpdateUserPassword, UserCourseListAPIView,
                        UserCreateAPIView, UserViewSet, UserTaskListAPIView)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('check/phone/', CheckPhoneAPIView.as_view({'post': 'list'}), name='check_phone'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('user/device/', DeviceModelListAPIView.as_view(), name='device-model-list'),
    path('user/register/', UserCreateAPIView.as_view(), name='token_obtain_pair'),
    path('user/login', LoginView.as_view(), name='token_login'),
    path('user/delete', DeleteUserAPIView.as_view(), name='deleted_user'),
    path('user/course/', UserCourseListAPIView.as_view(), name='user_course'),
    path('user/task/', UserTaskListAPIView.as_view(), name='user_task'),
    path('user/profile/', UpdateUser.as_view(), name='user_profile_update'),
    path('user/profile/password/', UpdateUserPassword.as_view(), name='user_profile_update'),

    path('course/module/', CourseModuleListAPIView.as_view(), name='course_module'),
    path('module/lesson/', ModuleLessonListAPIView.as_view(), name='module_lesson'),
]

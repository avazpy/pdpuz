from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.views import UserViewSet, RegisterCreateAPIView, UserCourseListAPIView, ModuleListAPIView, \
    LessonListAPIView, TaskListAPIView
from apps.views import UpdateUser

# from apps.views import LoginView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/register', RegisterCreateAPIView.as_view(), name='token_obtain_pair'),
    # path('users/login', LoginView.as_view(), name='token_login'),
    path('user-course', UserCourseListAPIView.as_view(), name='user_course'),
    path('module/', ModuleListAPIView.as_view(), name='module'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson'),
    path('task/', TaskListAPIView.as_view(), name='task'),
    path('user-profile-update:/<pk>', UpdateUser.as_view(), name='user_profile_update'),
]

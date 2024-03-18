from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import User, UserCourse, UserModule, UserLesson, UserTask


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options', 'country_model',
                   'has_registered_bot', 'not_read_message_count', 'ticket_role', 'voucher_balance', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance'
                   )

    def validate_password(self, password):
        return make_password(password)


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password')


class UserCreateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'password', 'email', 'phone_number'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        return make_password(password)


class UserCourseModelSerializer(ModelSerializer):
    class Meta:
        model = UserCourse
        fields = '__all__'


class UserModuleModelSerializer(ModelSerializer):
    class Meta:
        model = UserModule
        fields = '__all__'


class UserLessonModelSerializer(ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class UserTaskModelSerializer(ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

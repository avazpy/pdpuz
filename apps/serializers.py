from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import CharField

from apps.models import User, UserCourse, Lesson, Task, Module, Course, Device


# from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


# from apps.models import Profile


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options', 'country_model',
                   'has_registered_bot', 'not_read_message_count', 'ticket_role', 'voucher_balance', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance', 'last_login', 'username', 'first_name', 'last_name',
                   'date_joined'
                   )

    def validate_password(self, password):
        return make_password(password)


class UpdateUserSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'confirm_password', 'photo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            return data
        raise ValidationError("Password error")

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.set_password = validated_data.get('password', instance.password)
    #     instance.save()
    #     profile_data = validated_data.pop('profile')
    #     instance.profile.photo = profile_data.get('photo', instance.profile.photo)
    #     instance.profile.save()
    #
    #     return instance


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
        fields = 'created_at', 'user', 'course'


class ModuleModelSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = 'created_at', 'lesson_count', 'support_day', 'task_count', 'course'


class LessonModelSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'created_at', 'video_count', 'module', 'materials',


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = 'created_at', 'task_number', 'lastTime', 'files', 'lesson'


class CoursesModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = 'title', 'type', 'lesson_count', 'modul_count', 'task_count', 'order', 'task_count', 'url'


class DeviceModelSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class CheckPhoneModelSerializer(Serializer):
    phone_number = CharField(max_length=20, write_only=True)

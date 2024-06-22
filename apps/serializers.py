from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import (Course, DeletedUser, Device, Lesson, Module, Task,
                         User, UserCourse, UserLesson, UserModule, UserTask,
                         Video, )


class SingleDeviceLogin(Serializer):
    phone_number = CharField(label="Phone number")
    password = CharField(label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "phone_number" and "password".'
            raise ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options',
                   'has_registered_bot', 'not_read_message_count', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance', 'last_login', 'phone_number', 'email',
                   "tg_id", "type", 'date_joined', 'password', 'courses', 'username'
                   )

    def validate_password(self, password):
        return make_password(password)


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'photo'
        permission_classes = (IsAuthenticated,)


class UpdatePasswordUserSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = 'password', 'confirm_password'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        permission_classes = (IsAuthenticated,)

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            return data
        raise ValidationError("Password error")


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password')


class RegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'phone_number', 'password', 'confirm_password', 'first_name', 'last_name'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            return data
        raise ValidationError("Passwords don't match")

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Bu raqam allaqachon ro'xatda mavjud!")
        return phone_number


class UserCourseModelSerializer(ModelSerializer):
    class Meta:
        model = UserCourse
        fields = '__all__'

    def to_representation(self, instance: Course):
        represent = super().to_representation(instance)
        represent['modules'] = CourseModelSerializer(instance.module_set.all(), many=True).data
        return represent


class UserModuleModelSerializer(ModelSerializer):
    class Meta:
        model = UserModule
        fields = '__all__'


class UserCourseTeacherModelSerializer(ModelSerializer):

    class Meta:
        model = UserModule
        fields = '__all__'

    def to_representation(self, instance: UserModule):
        representation = super().to_representation(instance)
        representation['teacher'] = UserModelSerializer(instance.module.course).data
        return representation


class VideoModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = 'id', 'title'


class VideoGRUDSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class VideoDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        exclude = ()


class LessonModelSerializer(ModelSerializer):
    parts = VideoModelSerializer(source='video_set', many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = 'id', 'title', 'created_at', 'video_count', 'parts'

class LessonCRUDSerializer(ModelSerializer):
    parts = VideoModelSerializer(source='video_set', many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

class LessonDetailModelSerializer(ModelSerializer):
    parts = VideoDetailModelSerializer(source='video_set', many=True)

    class Meta:
        model = Lesson
        exclude = ('materials', 'is_deleted', 'slug')
        # fields = 'id', 'title', 'created_at', 'video_count', 'parts'


class ModuleModelSerializer(ModelSerializer):
    lessons = LessonModelSerializer(source='lesson_set', many=True)

    class Meta:
        model = Module
        fields = '__all__'


class ModuleCRUDSerializer(ModelSerializer):
    lessons = LessonModelSerializer(source='lesson_set', many=True)

    class Meta:
        model = Module
        fields = '__all__'


# class ModelSerializer(ModelSerializer):
#     teacher = UserModelSerializer(source='teacher_set',many=True,read_only=True)
#     class Meta:
#         model = Module
#         fields = '__all__'

class ModuleTeacherSerializer(ModelSerializer):
    # teacher = UserModelSerializer(source='teacher_set',many=True,read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ModuleLessonModelSerializer(ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = 'created_at', 'task_number', 'files', 'lesson', 'must_complete', 'title', 'description',


class TaskGRUDSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserTaskModelSerializer(ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

    def to_representation(self, instance: UserTask):
        representation = super().to_representation(instance)
        representation['task'] = TaskModelSerializer(instance.task).data
        return representation


class CourseModelSerializer(ModelSerializer):
    # teacher = UserModelSerializer(read_only=True)

    class Meta:
        model = Course
        fields = 'id', 'title', 'modul_count',


class CourseCRUDSerializer(ModelSerializer):
    # teacher = UserModelSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class DeviceModelSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class CheckPhoneModelSerializer(Serializer):
    phone_number = CharField(max_length=20, write_only=True)


class DeletedUserSerializer(ModelSerializer):
    class Meta:
        model = DeletedUser
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options',
                   'has_registered_bot', 'not_read_message_count', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance', 'last_login', 'email',
                   "tg_id", "photo", 'date_joined', 'username', 'password', 'courses',
                   )


class CustomDurinAuthSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'phone_number', 'password'


#
class AuthTokenSerializer(Serializer):
    phone_number = CharField(
        label=_("Phone number"),
        write_only=True
    )
    password = CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone_number" and "password".')
            raise ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomAuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=_("Phone number"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'), phone_number=phone_number, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone_number" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class MyUserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'photo'

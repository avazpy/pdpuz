from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import (Course, DeletedUser, Device, Lesson, Module, Task,
                         User, UserCourse, UserLesson, UserModule, UserTask)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options',
                   'has_registered_bot', 'not_read_message_count', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance', 'last_login', 'username', 'first_name', 'last_name',
                   'date_joined'
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

    def to_representation(self, instance: UserCourse):
        representation = super().to_representation(instance)
        representation['course_title'] = instance.course.title
        representation['lesson_count'] = instance.course.lesson_count
        representation['task_count'] = instance.course.task_count
        representation['modul_count'] = instance.course.modul_count
        return representation


class ModuleModelSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class UserModuleModelSerializer(ModelSerializer):
    class Meta:
        model = UserModule
        fields = '__all__'

    def to_representation(self, instance: UserModule):
        representation = super().to_representation(instance)
        representation['module_title'] = instance.module.title
        representation['lesson_count'] = instance.module.lesson_count
        representation['task_count'] = instance.module.task_count
        representation['modul_count'] = instance.module.pk
        return representation


class LessonModelSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'created_at', 'video_count', 'module', 'materials',


class ModuleLessonModelSerializer(ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = 'created_at', 'task_number', 'files', 'lesson'


class UserTaskModelSerializer(ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

    def to_representation(self, instance: UserTask):
        representation = super().to_representation(instance)
        representation['task_title'] = instance.task.title
        representation['task_number'] = instance.task.pk
        return representation


class CourseModelSerializer(ModelSerializer):
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

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import (Course, DeletedUser, Device, Lesson, Module, Task,
                         User, UserCourse, UserLesson, UserModule, UserTask, Video, )


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options',
                   'has_registered_bot', 'not_read_message_count', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance', 'last_login', 'username', 'email',
                   "tg_id", "type", 'date_joined', 'password', 'courses'
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
    updated_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

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

    def to_representation(self, instance: UserModule):
        representation = super().to_representation(instance)
        representation['module'] = ModuleModelSerializer(instance.module).data
        return representation


class UserCourseTeacherModelSerializer(ModelSerializer):
    # teacher = UserModelSerializer(source='module__course__teacher')

    class Meta:
        model = UserModule
        fields = '__all__'

    def to_representation(self, instance: UserModule):
        representation = super().to_representation(instance)
        representation['teacher'] = UserModelSerializer(instance.module.course.teacher).data
        return representation


class VideoModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = 'id', 'title'


class VideoDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        exclude = ()


class LessonModelSerializer(ModelSerializer):
    parts = VideoModelSerializer(source='video_set', many=True)

    class Meta:
        model = Lesson
        fields = 'id', 'title', 'created_at', 'video_count', 'parts'


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
        representation['task'] = TaskModelSerializer(instance.task).data
        return representation


class CourseModelSerializer(ModelSerializer):
    teacher = UserModelSerializer(read_only=True)

    class Meta:
        model = Course
        fields = 'id', 'title', 'modul_count', 'teacher'


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

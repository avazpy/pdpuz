from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import (Course, CourseModule, DeletedUser, Device, Lesson,
                         Module, Task, User, UserCourse, UserLesson)


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
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'photo'


class UpdatePasswordUserSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = 'password', 'confirm_password'
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


class ModuleModelSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = 'created_at', 'lesson_count', 'support_day', 'task_count', 'course'


class CourseModuleModelSerializer(ModelSerializer):
    class Meta:
        model = CourseModule
        fields = '__all__'


class LessonModelSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'created_at', 'video_count', 'module', 'materials',


class UserLessonModelSerializer(ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = 'created_at', 'task_number', 'files', 'lesson'


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


class DeletedUserSerializer(ModelSerializer):
    class Meta:
        model = DeletedUser
        fields = '__all__'




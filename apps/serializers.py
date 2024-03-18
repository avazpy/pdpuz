from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import User, UserCourse, UserModule, UserLesson, UserTask
# from apps.models import Profile


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'balance', 'bot_options', 'country_model',
                   'has_registered_bot', 'not_read_message_count', 'ticket_role', 'voucher_balance', 'is_active',
                   'is_superuser', 'is_staff', 'payme_balance'
                   )

    def validate_password(self, password):
        return make_password(password)


# class UpdateUserSerializer(ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'password', 'photo']
#
#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.set_password = validated_data.get('password', instance.password)
#         instance.save()
#         profile_data = validated_data.pop('profile')
#         instance.profile.photo = profile_data.get('photo', instance.profile.photo)
#         instance.profile.save()
#
#         return instance


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

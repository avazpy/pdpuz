from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password', 'photo', 'balance', 'bot_options', 'country_model',
                   'has_registered_bot', 'not_read_message_count', 'ticket_role', 'voucher_balance')


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password')


class UserCreateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'lastname', 'username', 'password', 'email'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        return make_password(password)

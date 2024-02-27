from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ()

#
# class UserDetailModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ('groups', 'user_permissions', 'password')
#
#
# class ProductListModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         exclude = ('description', 'category')
#
#
# class ProductModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         exclude = ()
#
#
# class CategoryModelSerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'parent')
#
#
# class UserCreateModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = 'username', 'email', 'password'
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def validate_password(self, password):
#         return make_password(password)

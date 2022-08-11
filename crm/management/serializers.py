from rest_framework.serializers import ModelSerializer
from .models import Users
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UsersDetailsSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'mobile', 'type']

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by management.

        :param value: password of a management
        :return: a hashed version of the password
        """
        return make_password(value)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Users.EMAIL_FIELD


class UserSerializer(ModelSerializer):
    """
       Serialize the model Users
    """
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'type', 'is_active', 'email', 'phone', 'mobile']

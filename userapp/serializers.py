from rest_framework.serializers import ModelSerializer
from .models import User


class UserModelSerializerReadOnly(ModelSerializer):

    class Meta:
        model = User
        fields = ['uuid', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser']


class UserModelSerializerWriteOnly(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active']

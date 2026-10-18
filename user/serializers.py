from rest_framework.serializers import ModelSerializer
from user.models import User


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'login', 'firstName', 'lastName', 'nickName', 'status', 'dateCreate', 'dateUpdate')
        read_only_fields = ('dateCreate',)


class UserNickNameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('nickName',)
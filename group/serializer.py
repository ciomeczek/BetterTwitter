from rest_framework import serializers
from .models import Group, GroupWaitList
from user.serializer import UserSerializer


class GroupDetailsSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    admins = UserSerializer(many=True, read_only=True)
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)


class GroupSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['name', 'description', 'image', 'is_member']

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)


class GroupWaitListSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()

    group = GroupSerializer()
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = GroupWaitList
        fields = ['group', 'members', 'is_member']

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)

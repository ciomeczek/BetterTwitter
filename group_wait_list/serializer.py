from rest_framework import serializers
from user.serializer import UserSerializer
from .models import GroupWaitList
from BetterTwitter.general_functions import validate_offset_and_limit


class GroupWaitListSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()

    members = serializers.SerializerMethodField()

    class Meta:
        model = GroupWaitList
        fields = ['id', 'group', 'members', 'is_member']

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)

    def get_members(self, group):
        offset, limit = validate_offset_and_limit(self.context.get('request'))

        qs = group.members.all()[offset: limit]

        serializer = UserSerializer(qs, many=True, read_only=True, context={'request': self.context.get('request')})

        return serializer.data

from rest_framework import serializers
from .models import Group
from user.serializer import UserSerializer


class GroupDetailsSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'image', 'is_member', 'members', 'admins']

    def get_members(self, group):
        offset, limit = validate_member_offset_and_limit(self.context.get('request'))

        qs = group.members.all().order_by('-pk')[offset:limit]

        serializer = UserSerializer(qs, many=True,
                                    read_only=True,
                                    context={'request': self.context.get('request')})

        return serializer.data

    def get_admins(self, group):
        offset, limit = validate_admins_offset_and_limit(self.context.get('request'))

        qs = group.admins.all().order_by('-pk')[offset:limit]

        serializer = UserSerializer(qs, many=True,
                                    read_only=True,
                                    context={'request': self.context.get('request')})

        return serializer.data

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)


class GroupSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'image', 'is_member']

    def get_is_member(self, group):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return group.is_user_group_member(user)


def validate_member_offset_and_limit(request):
    offset = request.query_params.get('memberoffset') or None
    limit = request.query_params.get('memberlimit') or None

    if offset is not None:
        offset = int(offset)

    if limit is not None:
        limit = int(limit)

    if offset is not None and limit is not None:
        limit = offset + limit

    return offset, limit


def validate_admins_offset_and_limit(request):
    offset = request.query_params.get('adminoffset') or None
    limit = request.query_params.get('adminlimit') or None

    if offset is not None:
        offset = int(offset)

    if limit is not None:
        limit = int(limit)

    if offset is not None and limit is not None:
        limit = offset + limit

    return offset, limit


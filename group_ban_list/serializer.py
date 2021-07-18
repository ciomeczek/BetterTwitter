from rest_framework import serializers
from .models import GroupBanList
from user.serializer import UserSerializer
from BetterTwitter.general_functions import validate_offset_and_limit


class GroupBanListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = GroupBanList
        fields = '__all__'

    def get_members(self, group):
        offset, limit = validate_offset_and_limit(self.context.get('request'))

        qs = group.members.all().order_by('-pk')[offset:limit]

        serializer = UserSerializer(qs, many=True,
                                    read_only=True,
                                    context={'request': self.context.get('request')})

        return serializer.data

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendList
from user_settings.serializer import FriendSettingsSerializer


class FriendSerializer(serializers.ModelSerializer):
    pfp = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()
    settings = FriendSettingsSerializer()

    class Meta:
        model = get_user_model()
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'full_name',
                  'pfp',
                  'settings']

    def get_pfp(self, user):
        request = self.context.get('request')
        pfp = user.pfp.url
        return request.build_absolute_uri(pfp)


class FriendListSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)

    class Meta:
        model = FriendList
        fields = ['friends']

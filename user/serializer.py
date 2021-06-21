from rest_framework import serializers
from django.contrib.auth import get_user_model
from friend.serializer import FriendListSerializer
from friend.models import FriendList, FriendRequest
from user_settings.serializer import SettingsSerializer


class UserSerializer(serializers.ModelSerializer):
    pfp = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()
    friends = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    is_request_from_me = serializers.SerializerMethodField()
    is_request_to_me = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'full_name',
                  'pfp',
                  'friends',
                  'is_friend',
                  'is_request_from_me',
                  'is_request_to_me']

    def get_pfp(self, user):
        request = self.context.get('request')
        pfp = user.pfp.url
        return request.build_absolute_uri(pfp)

    def get_friends(self, user):
        query_set = FriendList.objects.get(owner=user)
        return FriendListSerializer(query_set, context={'request': self.context.get('request')}).data.get('friends')

    def get_is_friend(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        friend_list = FriendList.objects.get(owner=user)
        return friend_list.is_friend(request_user)

    def get_is_request_from_me(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        return FriendRequest.objects.filter(sender=request_user, receiver=user).exists()

    def get_is_request_to_me(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        return FriendRequest.objects.filter(sender=user, receiver=request_user).exists()


class MeSerializer(serializers.ModelSerializer):
    pfp = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()
    friends = serializers.SerializerMethodField()
    settings = SettingsSerializer()
    is_friend = serializers.SerializerMethodField()
    is_request_from_me = serializers.SerializerMethodField()
    is_request_to_me = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'full_name',
                  'pfp',
                  'settings',
                  'friends',
                  'is_friend',
                  'is_request_from_me',
                  'is_request_to_me']

    def get_pfp(self, user):
        request = self.context.get('request')
        pfp = user.pfp.url
        return request.build_absolute_uri(pfp)

    def get_friends(self, user):
        query_set = FriendList.objects.get(owner=user)
        return FriendListSerializer(query_set, context={'request': self.context.get('request')}).data.get('friends')

    def get_is_friend(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        friend_list = FriendList.objects.get(owner=user)
        return friend_list.is_friend(request_user)

    def get_is_request_from_me(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        return FriendRequest.objects.filter(sender=request_user, receiver=user).exists()

    def get_is_request_to_me(self, user):
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            return False
        return FriendRequest.objects.filter(sender=user, receiver=request_user).exists()

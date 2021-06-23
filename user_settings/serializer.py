from rest_framework import serializers
from .models import UserSettings


class SettingsSerializer(serializers.ModelSerializer):
    account_status = serializers.SerializerMethodField()

    class Meta:
        model = UserSettings
        fields = ['account_status', 'can_get_invites']

    def get_account_status(self, settings):
        account_status = settings.account_status.status_name
        return account_status


class FriendSettingsSerializer(serializers.ModelSerializer):
    account_status = serializers.SerializerMethodField()

    class Meta:
        model = UserSettings
        fields = ['account_status', 'can_get_invites']

    def get_account_status(self, settings):
        account_status = settings.account_status.status_name
        return account_status

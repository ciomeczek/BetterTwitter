from rest_framework import serializers
from .models import PostReaction
from friend.serializer import FriendSerializer


class ReactionSerializer(serializers.ModelSerializer):
    owner = FriendSerializer(read_only=True)

    class Meta:
        model = PostReaction
        fields = ['owner']

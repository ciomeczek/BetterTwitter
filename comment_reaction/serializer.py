from rest_framework import serializers
from .models import CommentReaction
from friend.serializer import FriendSerializer


class ReactionSerializer(serializers.ModelSerializer):
    owner = FriendSerializer(read_only=True)

    class Meta:
        model = CommentReaction
        fields = ['owner']

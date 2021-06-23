from rest_framework import serializers
from .models import Comment, CommentImage
from friend.serializer import FriendSerializer


class CommentImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = CommentImage
        fields = ['url']

    def get_url(self, comment_image):
        request = self.context.get('request')
        img = comment_image.image.url
        return request.build_absolute_uri(img)


class CommentSerializer(serializers.ModelSerializer):
    author = FriendSerializer(read_only=True)
    images = CommentImageSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'description', 'created_at', 'images']

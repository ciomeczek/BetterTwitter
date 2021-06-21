from rest_framework import serializers
from .models import Post, PostImage
from friend.serializer import FriendSerializer
from comment.serializer import CommentSerializer
from comment.models import Comment
from post_reaction.models import PostReaction


class PostImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ['url']

    def get_url(self, post_image):
        request = self.context.get('request')
        image = post_image.image.url
        return request.build_absolute_uri(image)


class PostSerializer(serializers.ModelSerializer):
    author = FriendSerializer(read_only=True)
    images = PostImageSerializer(read_only=True, many=True)
    reaction_owners = FriendSerializer(read_only=True, many=True)
    reaction_count = serializers.SerializerMethodField()
    have_i_reacted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_reaction_count(self, post):
        return PostReaction.objects.filter(post=post).count()

    def get_have_i_reacted(self, post):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return PostReaction.objects.filter(owner=user, post=post).exists()


class PostDetailSerializer(serializers.ModelSerializer):
    author = FriendSerializer(read_only=True, many=False)
    images = PostImageSerializer(read_only=True, many=True)
    comments = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    have_i_reacted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, post):
        comments = Comment.objects.filter(post=post).order_by('created_at')
        return CommentSerializer(comments, many=True, context={'request': self.context.get('request')}).data

    def get_reaction_count(self, post):
        return PostReaction.objects.filter(post=post).count()

    def get_have_i_reacted(self, post):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return PostReaction.objects.filter(owner=user, post=post).exists()

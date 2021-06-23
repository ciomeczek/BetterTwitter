from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import PostReaction
from post.models import Post
from post import error_code


class Reactions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = post.author

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        if not PostReaction.objects.filter(post=post, owner=request.user).exists():
            PostReaction.objects.create(post=post, owner=request.user)
        return Response(status=201)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = post.author

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        PostReaction.objects.get(post=post, owner=request.user).delete()
        return Response(status=204)

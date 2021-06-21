from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PostReaction
from post.models import Post
from post import error_code


class AddReact(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get('post_id') is None:
            return Response(error_code.NO_POST_ID, status=400)

        post = Post.objects.get(pk=request.data.get('post_id'))
        user = post.author

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        if not PostReaction.objects.filter(post=post, owner=request.user).exists():
            PostReaction.objects.create(post=post, owner=request.user)
        return Response(status=201)


class DeleteReact(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        if request.data.get('post_id') is None:
            return Response(error_code.NO_POST_ID, status=400)

        post = Post.objects.get(pk=request.data.get('post_id'))
        user = post.author

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        PostReaction.objects.get(post=post, owner=request.user).delete()
        return Response(status=200)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CommentReaction
from comment.models import Comment
from comment import error_code


class AddReact(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get('comment_id') is None:
            return Response(error_code.NO_COMMENT_ID, status=400)

        comment = Comment.objects.get(pk=request.data.get('comment_id'))
        if not CommentReaction.objects.filter(comment=comment, owner=request.user).exists():
            CommentReaction.objects.create(comment=comment, owner=request.user)
        return Response(status=201)


class DeleteReact(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        if request.data.get('comment_id') is None:
            return Response(error_code.NO_COMMENT_ID, status=400)

        comment = Comment.objects.get(pk=request.data.get('comment_id'))
        CommentReaction.objects.get(
            comment=comment, owner=request.user).delete()
        return Response(status=200)

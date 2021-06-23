from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CommentReaction
from comment.models import Comment


class Reactions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if not CommentReaction.objects.filter(comment=comment, owner=request.user).exists():
            CommentReaction.objects.create(comment=comment, owner=request.user)
        return Response(status=201)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if CommentReaction.objects.filter(comment=comment, owner=request.user).exists():
            CommentReaction.objects.get(comment=comment, owner=request.user).delete()
        return Response(status=204)

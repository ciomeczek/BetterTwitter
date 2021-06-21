from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment, CommentImage
from post.models import Post
from .serializer import CommentSerializer
from . import error_code


class CreateComment(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, post_pk=None):
        post = get_object_or_404(Post, pk=post_pk)
        if request.data.get('description') is None and not request.FILES:
            return Response(error_code.NO_DESCRIPTION_AND_NO_FILES, status=400)

        # if one of files is description
        if 'description' in request.FILES:
            return Response(error_code.DESCRIPTION_IS_FILE, status=400)

        comment = Comment.objects.create(
            author=request.user, post=post, description=request.data.get('description'))

        for filename, file in request.FILES.items():
            CommentImage.objects.create(comment=comment, image=file)

        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=201)

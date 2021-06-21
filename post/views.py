from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Post, PostImage
from .serializer import PostSerializer, PostDetailSerializer
from . import error_code


def validate_offset_and_limit(request):
    offset = request.query_params.get('offset') or None
    limit = request.query_params.get('limit') or None

    try:
        if offset is not None:
            offset = int(offset)
    except ValueError:
        return Response(error_code.OFFSET_IS_NOT_INT, status=400)

    try:
        if limit is not None:
            limit = int(limit)
    except ValueError:
        return Response(error_code.LIMIT_IS_NOT_INT, status=400)

    if offset is not None and limit is not None:
        limit = offset + limit

    return offset, limit


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if request.data.get('description') is None and request.FILES is None:
            Response(error_code.NO_DESCRIPTION_AND_NO_FILES, status=400)

        # if one of files is description
        if 'description' in request.FILES:
            return Response(error_code.DESCRIPTION_IS_FILE, status=400)

        post = Post.objects.create(author=request.user, description=request.data.get('description'))

        for filename, file in request.FILES.items():
            PostImage.objects.create(post=post, image=file)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=201)


class SeePostsOfUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        offset, limit = validate_offset_and_limit(request)
        qs = Post.objects.filter(author=request.user).order_by('-created_at')[offset:limit]
        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class SeePostsOfUserByID(APIView):
    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        offset, limit = validate_offset_and_limit(request)

        qs = Post.objects.filter(author=user).order_by('-created_at')[offset:limit]
        serializer = PostSerializer(
            qs, many=True, context={'request': request})
        return Response(serializer.data)


class SeePostDetailsByID(APIView):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        user = post.author

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)


class HomePage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        offset = request.query_params.get('offset') or None
        limit = request.query_params.get('limit') or None
        post_id = request.query_params.get('post_id') or None

        try:
            if offset is not None:
                offset = int(offset)
        except ValueError:
            return Response(error_code.OFFSET_IS_NOT_INT, status=400)

        try:
            if limit is not None:
                limit = int(limit)
        except ValueError:
            return Response(error_code.LIMIT_IS_NOT_INT, status=400)

        try:
            if post_id is not None:
                post_id = int(post_id)
        except ValueError:
            return Response(error_code.POST_ID_IS_NOT_INT, status=400)

        if offset is not None and limit is not None:
            limit = offset + limit

        user_friends = request.user.friend_list.friends.all()

        if post_id is not None:
            post = get_object_or_404(Post, pk=post_id)
            from_date = post.created_at

            qs = Post.objects.filter(created_at__gte=from_date,
                                     author__in=user_friends).order_by('-created_at')[offset:limit]
        else:
            qs = Post.objects.filter(author__in=user_friends).order_by('-created_at')[offset:limit]

        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

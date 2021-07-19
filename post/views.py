from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Post, PostImage
from .serializer import PostSerializer, PostDetailSerializer
from . import error_code
from BetterTwitter.general_functions import validate_offset_and_limit


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
        qs = Post.objects.filter(author=request.user, group=None).order_by('-created_at')[offset:limit]
        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class SeePostsOfUserByID(APIView):
    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)

        if not Post.can_see_post(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        offset, limit = validate_offset_and_limit(request)

        qs = Post.objects.filter(author=user, group=None).order_by('-created_at')[offset:limit]
        serializer = PostSerializer(
            qs, many=True, context={'request': request})
        return Response(serializer.data)


class SeePostDetailsByID(APIView):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        user = post.author

        if not post.can_see_post_with_group(request_user=request.user, user=user):
            return Response(error_code.AUTHOR_IS_PRIVATE, status=403)

        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)


class HomePage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        post_id = request.query_params.get('post_id') or None

        try:
            if post_id is not None:
                post_id = int(post_id)
        except ValueError:
            return Response(error_code.POST_ID_IS_NOT_INT, status=400)

        offset, limit = validate_offset_and_limit(request)

        user_friends = request.user.friend_list.friends.all()

        if post_id is not None:
            post = get_object_or_404(Post, pk=post_id)
            from_date = post.created_at

            qs1 = Post.objects.filter(group__in=request.user.user_groups.all())
            qs2 = Post.objects.filter(group=None, author__in=user_friends, created_at__gte=from_date)
            qs = qs1.union(qs2).order_by('-created_at')[offset:limit]
        else:
            qs1 = Post.objects.filter(group__in=request.user.user_groups.all())
            qs2 = Post.objects.filter(group=None, author__in=user_friends)
            qs = qs1.union(qs2).order_by('-created_at')[offset:limit]

        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Group, GroupWaitList, GroupBanList
from .serializer import GroupSerializer, GroupDetailsSerializer
from . import error_code
from post.views import validate_offset_and_limit
from post.models import Post
from post.serializer import PostSerializer


class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        author = request.user

        if name is None:
            return Response(error_code.NO_NAME_FOR_GROUP_CREATION, status=400)

        if Group.objects.filter(name=name).exists():
            return Response(error_code.GROUP_NAME_ALREADY_EXISTS, status=400)

        group = Group.objects.create(name=name, description=description)
        group.members.add(author)
        group.admins.add(author)

        group.wait_list = GroupWaitList.objects.create()
        group.ban_list = GroupBanList.objects.create()

        group.save()

        return Response(status=201)


class DeleteGroup(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        group_wait_list = group.wait_list
        group_ban_list = group.ban_list

        group_wait_list.delete()
        group_ban_list.delete()
        group.delete()
        return Response(status=204)


class AddGroupImage(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        if request.FILES.get('image') is not None:
            img = request.FILES.get('image')
            group.image = img
            group.save()
            return Response(status=201)
        return Response(error_code.NO_GROUP_IMAGE, status=400)


class GetGroupDetails(APIView):
    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        qs = group

        serializer = GroupDetailsSerializer(qs, context={'request': request})

        return Response(serializer.data)


class GetGroupPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_member(request.user):
            return Response(error_code.USER_IS_NOT_MEMBER, status=403)

        post_id = request.query_params.get('post_id') or None

        offset, limit = validate_offset_and_limit(request)

        if post_id is not None:
            post = get_object_or_404(Post, pk=post_id)
            from_date = post.created_at

            qs = Post.objects.filter(group=group, created_at__gte=from_date).order_by('-created_at')[offset:limit]
        else:
            qs = Post.objects.filter(group=group).order_by('-created_at')[offset:limit]

        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class SearchGroup(APIView):
    def get(self, request):
        name = request.query_params.get('name')

        qs = Group.objects.filter(name__contains=name)

        serializer = GroupSerializer(qs, many=True, read_only=True, context={'request': request})

        return Response(serializer.data)


class AddSelfToWaitList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        group_wait_list = group.wait_list

        if request.user in group.ban_list.members.all():
            return Response(error_code.USER_IS_BANNED_FROM_GROUP, status=400)

        if group.is_user_group_member(request.user):
            return Response(error_code.USER_IS_ALREADY_MEMBER, status=400)

        group_wait_list.add_user(request.user)

        return Response(status=200)


class CancelSelfFromWaitList(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        group_wait_list = group.wait_list

        group_wait_list.remove_user(request.user)

        return Response(status=200)


class AcceptMemberFromWaitList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        group_wait_list = group.wait_list

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        user_to_accept_pk = request.data.get('user')

        if user_to_accept_pk is None:
            return Response(error_code.NO_USER_PK)

        if not get_user_model().objects.filter(pk=user_to_accept_pk).exists():
            return Response(error_code.USER_DOESNT_EXIST, status=404)

        user_to_accept = get_user_model().objects.get(pk=user_to_accept_pk)

        if user_to_accept not in group_wait_list.members.all():
            return Response(error_code.USER_NOT_IN_WAIT_LIST, status=400)

        group_wait_list.accept(user_to_accept)
        return Response(status=200)


class RemoveMemberFromWaitList(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        group_wait_list = group.wait_list

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        user_to_remove_pk = request.data.get('user')

        if user_to_remove_pk is None:
            return Response(error_code.NO_USER_PK)

        if not get_user_model().objects.filter(pk=user_to_remove_pk).exists():
            return Response(error_code.USER_DOESNT_EXIST, status=404)

        user_to_remove = get_user_model().objects.get(pk=user_to_remove_pk)

        if user_to_remove not in group_wait_list.members.all():
            return Response(error_code.USER_NOT_IN_WAIT_LIST, status=400)

        group_wait_list.remove_user(user_to_remove)
        return Response(status=200)


class BanMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        user_to_ban_pk = request.data.get('user')

        if user_to_ban_pk is None:
            return Response(error_code.NO_USER_PK)

        if not get_user_model().objects.filter(pk=user_to_ban_pk).exists():
            return Response(error_code.USER_DOESNT_EXIST, status=404)

        user_to_ban = get_user_model().objects.get(pk=user_to_ban_pk)

        if user_to_ban == request.user:
            return Response(error_code.USER_TO_BAN_IS_REQUEST_USER, status=400)

        group.ban_list.members.add(user_to_ban)
        return Response(status=200)


class UnBanMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        user_to_unban_pk = request.data.get('user')

        if user_to_unban_pk is None:
            return Response(error_code.NO_USER_PK)

        if not get_user_model().objects.filter(pk=user_to_unban_pk).exists():
            return Response(error_code.USER_DOESNT_EXIST, status=404)

        user_to_unban = get_user_model().objects.get(pk=user_to_unban_pk)

        group.ban_list.remove_user(user_to_unban)
        return Response(status=200)

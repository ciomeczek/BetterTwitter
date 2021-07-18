from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from group.models import Group
from group import error_code
from .serializer import GroupWaitListSerializer


class GetGroupWaitList(APIView):
    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        serializer = GroupWaitListSerializer(group.wait_list, context={'request': request})

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


class AcceptUserFromWaitList(APIView):
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


class RemoveUserFromWaitList(APIView):
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
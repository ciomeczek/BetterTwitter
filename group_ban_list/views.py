from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from group.models import Group
from group import error_code
from .serializer import GroupBanListSerializer


class GetBanList(APIView):
    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        if not group.is_user_group_admin(request.user):
            return Response(error_code.USER_IS_NOT_ADMIN, status=403)

        serializer = GroupBanListSerializer(group.ban_list, context={'request': request})

        return Response(serializer.data)


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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import FriendRequest, FriendList
from . import error_code


class InviteFriend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get('receiver') is None:
            return Response(error_code.NO_RECEIVER, status=400)

        receiver = get_user_model().objects.get(pk=request.data.get('receiver'))
        sender = request.user

        created = FriendRequest.invite(sender=sender, receiver=receiver).get('created')

        if created:
            return Response(status=201)
        return Response(status=200)


class AcceptFriend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get('receiver') is None:
            return Response(error_code.NO_RECEIVER, status=400)

        receiver = request.user
        sender = get_user_model().objects.get(pk=request.data.get('receiver'))
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.get(sender=sender, receiver=receiver).accept()

        return Response(status=200)


class RejectFriend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get('receiver') is None:
            return Response(error_code.NO_RECEIVER, status=400)

        sender = get_user_model().objects.get(pk=request.data.get('receiver'))
        receiver = request.user
        # try:
        #     FriendRequest.objects.get(sender=sender, receiver=receiver).decline()
        # except FriendRequest.DoesNotExist:
        #     return Response(status=200)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.get(sender=sender, receiver=receiver).decline()

        return Response(status=200)


class CancelRequest(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        if request.data.get('receiver') is None:
            return Response(error_code.NO_RECEIVER, status=400)

        receiver = get_user_model().objects.get(pk=request.data.get('receiver'))
        sender = request.user
        # try:
        #     FriendRequest.objects.get(sender=sender, receiver=receiver).decline()
        # except FriendRequest.DoesNotExist:
        #     return Response(status=200)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.get(sender=sender, receiver=receiver).decline()

        return Response(status=200)


class RemoveFriend(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        if request.data.get('friend') is None:
            return Response(error_code.NO_FRIEND, status=400)

        friend = get_user_model().objects.get(pk=request.data.get('friend'))
        user = request.user

        user_friend_list = FriendList.objects.get(owner=user)

        user_friend_list.unfriend(friend)
        return Response(status=204)

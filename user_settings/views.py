from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import error_code


class SetSettings(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        if request.data.get('account_status'):
            account_status = request.data.get('account_status')
            if 1 > account_status or account_status > 3:
                return Response(error_code.INVALID_ACCOUNT_STATUS, status=400)
            request.user.settings.set_account_status(account_status)
            return Response(status=204)

        if request.data.get('can_get_invites'):
            can_get_invites = request.data.get('can_get_invites')
            if isinstance(can_get_invites, bool):
                request.user.settings.can_get_invites = request.data.get('can_get_invites')
                return Response(status=204)
            return Response(error_code.CAN_GET_INVITES_NOT_BOOL, status=400)

        return Response(status=200)

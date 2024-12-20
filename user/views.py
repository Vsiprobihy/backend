from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.models import CustomUser
from custom_admin.models import OrganizerRequest
from utils.custom_exceptions import BadRequestError, CreatedResponse


class RequestOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_id):  # noqa
        user = CustomUser.objects.filter(id=member_id).first()

        if not user:
            return BadRequestError('User not found.').get_response()

        if OrganizerRequest.objects.filter(user=user, is_approved=False).exists():
            return BadRequestError('You already have a pending request.').get_response()

        OrganizerRequest.objects.create(user=user)
        return CreatedResponse('Request submitted successfully.').get_response()
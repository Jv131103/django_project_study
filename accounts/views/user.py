from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.views.base import Base


class GetUser(Base):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()

        enterprise = self.get_enterprise_user(user)

        serializer = UserSerializer(user)

        return Response(
            {
                "user": serializer.data,
                "enterprise": enterprise
            }
        )

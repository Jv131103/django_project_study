from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.auth import Autentication
from accounts.serializers import UserSerializer
from accounts.views.base import Base


class Signin(Base):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = Autentication.signin(self, email=email, password=password)

        token = RefreshToken.for_user(user)

        enterprise = self.get_enterprise_user(user.id)

        serializer = UserSerializer(user)

        return Response(
            {
                "user": serializer.data,
                "enterprise": enterprise,
                "refresh": str(token),
                "access": str(token.access_token)
            }
        )

from rest_framework.response import Response

from accounts.auth import Autentication
from accounts.serializers import UserSerializer
from accounts.views.base import Base


class Signup(Base):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        user = Autentication.signup(
            self,
            name=name,
            email=email,
            password=password
        )

        serializer = UserSerializer(user)

        return Response(
            {
                "user": serializer.data
            }
        )

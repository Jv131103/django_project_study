from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import APIException, AuthenticationFailed

from accounts.models import User
from companies.models import Employee, Enterprise


class Autentication:
    def signin(self, email=None, password=None) -> User | None:
        exception_auth = AuthenticationFailed(
                f"Usuário de email {email} não encontrado "
                "Verifique o email/senha e tente novamente."
            )
        user_exists = User.objects.filter(email=email).first()

        if not user_exists:
            raise exception_auth

        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth

        return user

    def signup(
            self,
            name=None,
            email=None,
            password=None,
            type_account="",
            company_id=False
    ) -> User | None:

        if not name:
            raise APIException("O nome é obrigatório, não pode ser vazio.")

        if not email:
            raise APIException("O email é obrigatório, não pode ser vazio.")

        if not password:
            raise APIException("A senha é obrigatória, não pode ser vazia.")

        if type_account == "employ" and not company_id:
            raise APIException(
                "O id da empresa é obrigatório para criar um "
                "usuário do tipo funcionário."
            )

        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            raise APIException(
                f"Usuário de email {email} já existe."
            )

        password_hash = make_password(password)

        create_user = User.objects.create(
            name=name,
            email=email,
            password=password_hash,
            is_owner=0 if type_account == "employ" else 1
        )

        if type_account == "owner":
            created_enterprise = Enterprise.objects.create(
                name="Nome da empresa",
                user_id=create_user.id,
            )

        if type_account == "employ":
            Employee.objects.create(
                user_id=create_user.id,
                enterprise_id=company_id or created_enterprise.id,
            )

        return create_user

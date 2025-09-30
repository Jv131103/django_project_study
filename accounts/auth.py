from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import \
    ValidationError  # melhor que APIException para input inválido
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User
from companies.models import Employee, Enterprise


class Autentication:
    def signin(self, email=None, password=None) -> User | None:
        exc = AuthenticationFailed(
            f"Usuário de email {email} não encontrado. "
            "Verifique email/senha e tente novamente."
        )
        user = User.objects.filter(email=email).first()
        if not user:
            raise exc
        if not check_password(password, user.password):
            raise exc
        return user

    def signup(
        self,
        name=None,
        email=None,
        password=None,
        type_account="owner",  # defina um padrão explícito
        company_id=None
    ) -> User:
        if not name:
            raise ValidationError({"name": "O nome é obrigatório."})
        if not email:
            raise ValidationError({"email": "O email é obrigatório."})
        if not password:
            raise ValidationError({"password": "A senha é obrigatória."})
        if type_account == "employ" and not company_id:
            raise ValidationError({"company_id": "Obrigatório para funcionário."})

        # ✅ lógica correta
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": f"Já existe um usuário com {email}."})

        password_hash = make_password(password)

        user = User.objects.create(
            name=name,
            email=email,
            password=password_hash,
            is_owner=(type_account == "owner"),
        )

        if type_account == "owner":
            created_enterprise = Enterprise.objects.create(
                name="Nome da empresa",
                user_id=user.id,
            )

        if type_account == "employ":
            # se vier company_id usa, senão usa da criada acima
            Employee.objects.create(
                user_id=user.id,
                enterprise_id=company_id or created_enterprise.id,
            )

        return user

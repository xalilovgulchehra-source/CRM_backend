from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:
    @staticmethod
    def register_user(
        email, password, role="OWNER", full_name="", salon_name="", owner_name="", phone=""
    ):
        if User.objects.filter(email=email).exists():
            raise ValueError("Bu email allaqachon ro'yxatdan o'tgan")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            full_name=full_name,
            salon_name=salon_name,
            owner_name=owner_name,
            phone=phone,
        )
        return user

    @staticmethod
    def generate_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def authenticate(email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    @staticmethod
    def user_data(user):
        data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "fullName": user.full_name,
            "phone": user.phone,
            "createdAt": user.created_at.isoformat().replace("+00:00", "Z")
            if user.created_at
            else None,
        }
        if user.role == User.Role.OWNER:
            data["salonName"] = user.salon_name
            data["ownerName"] = user.owner_name
        return data

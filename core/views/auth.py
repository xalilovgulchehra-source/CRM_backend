from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from ..services.auth_service import AuthService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = AuthService.register_user(
                email=data["email"],
                password=data["password"],
                role=data.get("role", "OWNER"),
                full_name=data.get("full_name", ""),
                salon_name=data.get("salon_name", ""),
                owner_name=data.get("owner_name", ""),
                phone=data["phone"],
            )
        except ValueError as e:
            return Response({"xato": str(e)}, status=status.HTTP_409_CONFLICT)

        token = AuthService.generate_token(user)

        return Response(
            {
                "token": token,
                "foydalanuvchi": AuthService.user_data(user),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = AuthService.authenticate(
            email=data["email"],
            password=data["password"],
        )

        if user is None:
            return Response(
                {"xato": "Email yoki parol noto'g'ri"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = AuthService.generate_token(user)

        return Response(
            {
                "token": token,
                "foydalanuvchi": AuthService.user_data(user),
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"foydalanuvchi": AuthService.user_data(request.user)},
            status=status.HTTP_200_OK,
        )

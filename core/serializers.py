from rest_framework import serializers
from .models import User, Client, Service, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "salon_name", "owner_name", "phone", "created_at"]
        read_only_fields = ["id", "created_at"]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"invalid": "Noto'g'ri email manzil"})
    password = serializers.CharField(
        min_length=6,
        error_messages={"blank": "Parol kiritilishi shart"},
    )
    salon_name = serializers.CharField(
        error_messages={"blank": "Salon nomi kiritilishi shart"},
    )
    owner_name = serializers.CharField(
        error_messages={"blank": "Egasi ismi kiritilishi shart"},
    )
    phone = serializers.CharField(
        error_messages={"blank": "Telefon raqami kiritilishi shart"},
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro'yxatdan o'tgan")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "full_name",
            "phone",
            "notes",
            "last_visit",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "last_visit"]


class ClientCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        error_messages={"blank": "Mijoz ismi kiritilishi shart"},
    )
    phone = serializers.CharField(
        error_messages={"blank": "Telefon raqami kiritilishi shart"},
    )
    notes = serializers.CharField(required=False, allow_blank=True, default=None)


class ClientUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True, default=None)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "price", "duration_mins", "created_at"]
        read_only_fields = ["id", "created_at"]


class ServiceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(
        error_messages={"blank": "Xizmat nomi kiritilishi shart"},
    )
    price = serializers.IntegerField(
        error_messages={"invalid": "Narx musbat son bo'lishi kerak"},
    )
    duration_mins = serializers.IntegerField(
        error_messages={"invalid": "Davomiylik musbat butun son bo'lishi kerak"},
    )


class ServiceUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    duration_mins = serializers.IntegerField(required=False)


class ClientBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "full_name",
            "phone",
            "notes",
            "last_visit",
            "created_at",
        ]


class ServiceBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "price", "duration_mins", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    client = ClientBriefSerializer(read_only=True)
    service = ServiceBriefSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "client_id",
            "client",
            "service_id",
            "service",
            "date",
            "status",
            "notes",
            "price",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "client_id", "service_id"]


class BookingCreateSerializer(serializers.Serializer):
    client_id = serializers.IntegerField(
        error_messages={"invalid": "Mijoz ID musbat son bo'lishi kerak"},
    )
    service_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None,
        error_messages={"invalid": "Xizmat ID musbat son bo'lishi kerak"},
    )
    date = serializers.DateTimeField(
        error_messages={"blank": "Sana kiritilishi shart"},
    )
    price = serializers.IntegerField(
        error_messages={"invalid": "Narx musbat son bo'lishi kerak"},
    )
    notes = serializers.CharField(required=False, allow_blank=True, default=None)
    status = serializers.ChoiceField(
        choices=Booking.Status.choices,
        required=False,
        default=Booking.Status.PENDING,
    )


class BookingUpdateSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(choices=Booking.Status.choices, required=False)
    notes = serializers.CharField(required=False, allow_blank=True, default=None)
    price = serializers.IntegerField(required=False)
    client_id = serializers.IntegerField(required=False)
    service_id = serializers.IntegerField(required=False, allow_null=True, default=None)
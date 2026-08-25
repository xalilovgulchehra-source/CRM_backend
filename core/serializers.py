from rest_framework import serializers
from .models import User, Client, Service, Booking, ChatMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "full_name",
            "salon_name",
            "owner_name",
            "phone",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"invalid": "Noto'g'ri email manzil"})
    password = serializers.CharField(
        min_length=6,
        error_messages={"blank": "Parol kiritilishi shart"},
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=False,
        default=User.Role.OWNER,
    )
    full_name = serializers.CharField(required=False, allow_blank=True, default="")
    fullName = serializers.CharField(required=False, allow_blank=True, default="", write_only=True)
    salon_name = serializers.CharField(required=False, allow_blank=True, default="")
    salonName = serializers.CharField(required=False, allow_blank=True, default="", write_only=True)
    owner_name = serializers.CharField(required=False, allow_blank=True, default="")
    ownerName = serializers.CharField(required=False, allow_blank=True, default="", write_only=True)
    phone = serializers.CharField(
        error_messages={"blank": "Telefon raqami kiritilishi shart"},
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro'yxatdan o'tgan")
        return value

    def validate(self, data):
        if not data.get("full_name") and data.get("fullName"):
            data["full_name"] = data["fullName"]
        if not data.get("salon_name") and data.get("salonName"):
            data["salon_name"] = data["salonName"]
        if not data.get("owner_name") and data.get("ownerName"):
            data["owner_name"] = data["ownerName"]

        role = data.get("role", User.Role.OWNER)
        if role == User.Role.OWNER:
            if not data.get("salon_name"):
                raise serializers.ValidationError(
                    {"salonName": "Salon nomi kiritilishi shart"}
                )
            if not data.get("owner_name"):
                raise serializers.ValidationError(
                    {"ownerName": "Egasi ismi kiritilishi shart"}
                )
        elif role == User.Role.CUSTOMER:
            if not data.get("full_name"):
                raise serializers.ValidationError(
                    {"fullName": "To'liq ism kiritilishi shart"}
                )
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "salon_name", "owner_name", "phone"]


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


class CustomerBookingCreateSerializer(serializers.Serializer):
    service_id = serializers.IntegerField(
        error_messages={"invalid": "Xizmat ID musbat son bo'lishi kerak"},
    )
    serviceId = serializers.IntegerField(
        required=False,
        write_only=True,
    )
    date = serializers.DateTimeField(
        error_messages={"blank": "Sana kiritilishi shart"},
    )
    notes = serializers.CharField(required=False, allow_blank=True, default=None)

    def validate(self, data):
        if not data.get("service_id") and data.get("serviceId"):
            data["service_id"] = data["serviceId"]
        return data


class ServicePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "price", "duration_mins"]


class MyBookingSerializer(serializers.ModelSerializer):
    service = ServicePublicSerializer(read_only=True)
    salon_name = serializers.CharField(source="user.salon_name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "salon_name",
            "service",
            "date",
            "status",
            "notes",
            "price",
            "created_at",
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    sender_email = serializers.CharField(source="sender.email", read_only=True)
    sender_role = serializers.CharField(source="sender.role", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "sender",
            "sender_name",
            "sender_email",
            "sender_role",
            "text",
            "is_read",
            "created_at",
        ]
        read_only_fields = ["id", "sender", "is_read", "created_at"]


class ChatSendSerializer(serializers.Serializer):
    text = serializers.CharField(
        error_messages={"blank": "Xabar matni kiritilishi shart"},
    )

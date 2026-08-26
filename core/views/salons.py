from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..models import User, Client, Service, Booking
from ..serializers import (
    SalonSerializer,
    ServicePublicSerializer,
    CustomerBookingCreateSerializer,
    MyBookingSerializer,
)


class SalonListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        salons = User.objects.filter(
            role=User.Role.OWNER,
            salon_name__in=["MySalon", "StyleShop"],
        ).order_by("-created_at")
        serializer = SalonSerializer(salons, many=True)
        return Response(
            {
                "salonlar": serializer.data,
                "soni": salons.count(),
            },
            status=status.HTTP_200_OK,
        )


class SalonServiceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, salon_id):
        salon = get_object_or_404(
            User.objects.filter(role=User.Role.OWNER),
            pk=salon_id,
        )
        services = Service.objects.filter(user=salon).order_by("-created_at")
        serializer = ServicePublicSerializer(services, many=True)
        return Response(
            {
                "xizmatlar": serializer.data,
                "soni": services.count(),
            },
            status=status.HTTP_200_OK,
        )


class CustomerBookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, salon_id):
        if request.user.role != User.Role.CUSTOMER:
            return Response(
                {"xato": "Faqat mijozlar buyurtma berishi mumkin"},
                status=status.HTTP_403_FORBIDDEN,
            )

        salon = get_object_or_404(
            User.objects.filter(role=User.Role.OWNER),
            pk=salon_id,
        )

        serializer = CustomerBookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = get_object_or_404(
            Service.objects.filter(user=salon),
            pk=data["service_id"],
        )

        client, _ = Client.objects.get_or_create(
            user=salon,
            phone=request.user.phone,
            defaults={
                "full_name": request.user.full_name,
                "phone": request.user.phone,
            },
        )

        booking = Booking.objects.create(
            date=data["date"],
            status=Booking.Status.PENDING,
            notes=data.get("notes", ""),
            price=service.price,
            client=client,
            service=service,
            user=salon,
            customer=request.user,
        )

        return Response(
            {"navbat": MyBookingSerializer(booking).data},
            status=status.HTTP_201_CREATED,
        )


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.CUSTOMER:
            return Response(
                {"xato": "Faqat mijozlar uchun"},
                status=status.HTTP_403_FORBIDDEN,
            )

        bookings = Booking.objects.filter(
            customer=request.user,
        ).select_related("service", "user").order_by("-date")

        serializer = MyBookingSerializer(bookings, many=True)
        return Response(
            {
                "navbatlar": serializer.data,
                "soni": bookings.count(),
            },
            status=status.HTTP_200_OK,
        )

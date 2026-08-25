from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..models import Booking, Client
from ..serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    BookingUpdateSerializer,
)


class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Booking.objects.filter(user=request.user)

        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        queryset = queryset.order_by("date")
        serializer = BookingSerializer(queryset, many=True)

        return Response(
            {
                "navbatlar": serializer.data,
                "soni": queryset.count(),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        client = get_object_or_404(
            Client.objects.filter(user=request.user),
            pk=data["client_id"],
        )

        service = None
        if data.get("service_id"):
            from ..models import Service

            service = get_object_or_404(
                Service.objects.filter(user=request.user),
                pk=data["service_id"],
            )

        booking = Booking.objects.create(
            date=data["date"],
            status=data.get("status", Booking.Status.PENDING),
            notes=data.get("notes"),
            price=data["price"],
            client=client,
            service=service,
            user=request.user,
        )

        client.last_visit = timezone.now()
        client.save(update_fields=["last_visit"])

        return Response(
            {"navbat": BookingSerializer(booking).data},
            status=status.HTTP_201_CREATED,
        )


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        booking = get_object_or_404(
            Booking.objects.filter(user=request.user),
            pk=pk,
        )
        return Response(
            {"navbat": BookingSerializer(booking).data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        booking = get_object_or_404(
            Booking.objects.filter(user=request.user),
            pk=pk,
        )

        serializer = BookingUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "date" in data:
            booking.date = data["date"]
        if "status" in data:
            booking.status = data["status"]
        if "notes" in data:
            booking.notes = data["notes"]
        if "price" in data:
            booking.price = data["price"]
        if "client_id" in data:
            client = get_object_or_404(
                Client.objects.filter(user=request.user),
                pk=data["client_id"],
            )
            booking.client = client
        if "service_id" in data:
            if data["service_id"] is None:
                booking.service = None
            else:
                from ..models import Service

                service = get_object_or_404(
                    Service.objects.filter(user=request.user),
                    pk=data["service_id"],
                )
                booking.service = service

        booking.save()

        return Response(
            {"navbat": BookingSerializer(booking).data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        booking = get_object_or_404(
            Booking.objects.filter(user=request.user),
            pk=pk,
        )
        booking.delete()
        return Response(
            {"xabar": "Navbat muvaffaqiyatli o'chirildi"},
            status=status.HTTP_200_OK,
        )

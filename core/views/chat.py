from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Booking, ChatMessage
from ..serializers import ChatMessageSerializer, ChatSendSerializer


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)

        if request.user != booking.user and request.user != booking.customer:
            return Response(
                {"xato": "Sizda bu zakazga ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN,
            )

        messages = ChatMessage.objects.filter(booking=booking).select_related("sender")
        serializer = ChatMessageSerializer(messages, many=True)

        unread_count = messages.filter(is_read=False).exclude(sender=request.user).count()

        return Response(
            {
                "xabarlar": serializer.data,
                "soni": messages.count(),
                "o_qilmagan": unread_count,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)

        if request.user != booking.user and request.user != booking.customer:
            return Response(
                {"xato": "Sizda bu zakazga ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ChatSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        message = ChatMessage.objects.create(
            booking=booking,
            sender=request.user,
            text=data["text"],
        )

        return Response(
            {"xabar": ChatMessageSerializer(message).data},
            status=status.HTTP_201_CREATED,
        )


class ChatReadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)

        if request.user != booking.user and request.user != booking.customer:
            return Response(
                {"xato": "Sizda bu zakazga ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN,
            )

        updated = ChatMessage.objects.filter(
            booking=booking,
        ).exclude(sender=request.user).update(is_read=True)

        return Response(
            {"xabar": f"{updated} ta xabar o'qilgan deb belgilandi"},
            status=status.HTTP_200_OK,
        )

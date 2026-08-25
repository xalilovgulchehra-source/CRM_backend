from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import Client
from ..serializers import (
    ClientSerializer,
    ClientCreateSerializer,
    ClientUpdateSerializer,
)


class ClientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        queryset = Client.objects.filter(user=request.user)

        if q:
            queryset = queryset.filter(
                Q(full_name__icontains=q) | Q(phone__icontains=q)
            )

        queryset = queryset.order_by("-created_at")
        serializer = ClientSerializer(queryset, many=True)

        return Response(
            {
                "mijozlar": serializer.data,
                "soni": queryset.count(),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        client = Client.objects.create(
            full_name=data["full_name"],
            phone=data["phone"],
            notes=data.get("notes"),
            user=request.user,
        )

        return Response(
            {"mijoz": ClientSerializer(client).data},
            status=status.HTTP_201_CREATED,
        )


class ClientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object_or_404(
            Client.objects.filter(user=request.user),
            pk=pk,
        )
        return Response(
            {"mijoz": ClientSerializer(client).data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        client = get_object_or_404(
            Client.objects.filter(user=request.user),
            pk=pk,
        )

        serializer = ClientUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "full_name" in data:
            client.full_name = data["full_name"]
        if "phone" in data:
            client.phone = data["phone"]
        if "notes" in data:
            client.notes = data["notes"]

        client.save()

        return Response(
            {"mijoz": ClientSerializer(client).data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        client = get_object_or_404(
            Client.objects.filter(user=request.user),
            pk=pk,
        )
        client.delete()
        return Response(
            {"xabar": "Mijoz muvaffaqiyatli o'chirildi"},
            status=status.HTTP_200_OK,
        )

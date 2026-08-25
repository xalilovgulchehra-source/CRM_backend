from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Service
from ..serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
)


class ServiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Service.objects.filter(user=request.user).order_by("-created_at")
        serializer = ServiceSerializer(queryset, many=True)

        return Response(
            {
                "xizmatlar": serializer.data,
                "soni": queryset.count(),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ServiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = Service.objects.create(
            name=data["name"],
            price=data["price"],
            duration_mins=data["duration_mins"],
            user=request.user,
        )

        return Response(
            {"xizmat": ServiceSerializer(service).data},
            status=status.HTTP_201_CREATED,
        )


class ServiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        service = get_object_or_404(
            Service.objects.filter(user=request.user),
            pk=pk,
        )
        return Response(
            {"xizmat": ServiceSerializer(service).data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        service = get_object_or_404(
            Service.objects.filter(user=request.user),
            pk=pk,
        )

        serializer = ServiceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "name" in data:
            service.name = data["name"]
        if "price" in data:
            service.price = data["price"]
        if "duration_mins" in data:
            service.duration_mins = data["duration_mins"]

        service.save()

        return Response(
            {"xizmat": ServiceSerializer(service).data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        service = get_object_or_404(
            Service.objects.filter(user=request.user),
            pk=pk,
        )
        service.delete()
        return Response(
            {"xabar": "Xizmat muvaffaqiyatli o'chirildi"},
            status=status.HTTP_200_OK,
        )

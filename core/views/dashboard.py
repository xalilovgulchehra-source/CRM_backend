from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..services.dashboard_service import DashboardService


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = DashboardService.get_stats(request.user)
        return Response(stats, status=status.HTTP_200_OK)

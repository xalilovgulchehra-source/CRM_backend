from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


@api_view(["GET"])
def health_check(request):
    return Response({
        "holat": "faol",
        "xizmat": "Salon CRM API",
        "vaqt": datetime.utcnow().isoformat() + "Z",
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", health_check, name="health-check"),
    path("api/", include("core.urls")),
]

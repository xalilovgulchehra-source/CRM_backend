from django.urls import path

from .views.auth import RegisterView, LoginView, MeView
from .views.clients import ClientListView, ClientDetailView
from .views.services import ServiceListView, ServiceDetailView
from .views.bookings import BookingListView, BookingDetailView
from .views.dashboard import DashboardStatsView
from .views.salons import (
    SalonListView,
    SalonServiceListView,
    CustomerBookingCreateView,
    MyBookingsView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("salons/", SalonListView.as_view(), name="salon-list"),
    path(
        "salons/<int:salon_id>/services/",
        SalonServiceListView.as_view(),
        name="salon-services",
    ),
    path(
        "salons/<int:salon_id>/bookings/",
        CustomerBookingCreateView.as_view(),
        name="customer-booking-create",
    ),
    path("my-bookings/", MyBookingsView.as_view(), name="my-bookings"),
]

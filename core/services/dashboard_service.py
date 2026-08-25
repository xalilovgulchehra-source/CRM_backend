from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class DashboardService:
    @staticmethod
    def get_stats(user):
        today = timezone.localdate()
        today_start = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )
        today_end = timezone.make_aware(
            timezone.datetime.combine(today + timedelta(days=1), timezone.datetime.min.time())
        )

        total_clients = user.clients.count()
        total_services = user.services.count()
        total_bookings = user.bookings.count()
        today_bookings = user.bookings.filter(
            date__gte=today_start,
            date__lt=today_end,
        ).count()

        return {
            "totalClients": total_clients,
            "totalServices": total_services,
            "totalBookings": total_bookings,
            "todayBookings": today_bookings,
        }

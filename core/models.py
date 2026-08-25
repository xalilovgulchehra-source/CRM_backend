from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers.user_manager import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Salon egasi"
        CUSTOMER = "CUSTOMER", "Mijoz"

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OWNER,
        verbose_name="Rol",
    )
    full_name = models.CharField(
        max_length=255, blank=True, default="", verbose_name="To'liq ism"
    )
    salon_name = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Salon nomi"
    )
    owner_name = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Egasi ismi"
    )
    phone = models.CharField(max_length=50, verbose_name="Telefon")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.email


class Client(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism")
    phone = models.CharField(max_length=50, verbose_name="Telefon")
    notes = models.TextField(blank=True, null=True, verbose_name="Eslatmalar")
    last_visit = models.DateTimeField(blank=True, null=True, verbose_name="Oxirgi tashrif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Foydalanuvchi",
    )

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Xizmat nomi")
    price = models.PositiveIntegerField(verbose_name="Narx")
    duration_mins = models.PositiveIntegerField(verbose_name="Davomiylik (daqiqa)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Foydalanuvchi",
    )

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Kutilmoqda"
        CONFIRMED = "CONFIRMED", "Tasdiqlangan"
        DONE = "DONE", "Bajarilgan"
        CANCELLED = "CANCELLED", "Bekor qilingan"

    date = models.DateTimeField(verbose_name="Sana va vaqt")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Holat",
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Eslatmalar")
    price = models.PositiveIntegerField(verbose_name="Narx")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Mijoz",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        verbose_name="Xizmat",
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_bookings",
        verbose_name="Buyurtma beruvchi mijoz",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Foydalanuvchi",
    )

    class Meta:
        verbose_name = "Navbat"
        verbose_name_plural = "Navbatlar"
        ordering = ["date"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.client.full_name} - {self.date}"


class ChatMessage(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Navbat",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Yuboruvchi",
    )
    text = models.TextField(verbose_name="Xabar matni")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Chat xabari"
        verbose_name_plural = "Chat xabarlari"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.email}: {self.text[:50]}"

from django.contrib import admin
from .models import User, Client, Service, Booking

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Booking)

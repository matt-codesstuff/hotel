from django.contrib import admin

from .models import Guest, Booking, Room

admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Room)

from django.contrib import admin

from .models import Guest, Booking, Room, Floor

admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Floor)

from django.db import models

from django.utils import timezone


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    tel_number = models.CharField(max_length=12, blank=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Room(models.Model):
    identifier = models.CharField(max_length=8)
    occupancy = models.IntegerField()

    def __str__(self):
        return self.identifier    
    

class Booking(models.Model):
    main_guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, default=None)
    total_guests = models.IntegerField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    check_in = models.DateTimeField('check-in', default=timezone.now)
    check_out = models.DateTimeField('check-out')

    def __str__(self):
        return f'{self.main_guest}'    
    # had to write this method because django scripting has no built-in
    # method for checking if an item is a num(int)
    def isnum(self):
        return self.room.identifier.isdigit()


    
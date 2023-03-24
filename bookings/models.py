import datetime

from django.db import models
from django.utils import timezone


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    tel_number = models.CharField(max_length=12, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        if self.last_name:
            return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
        else: 
            return f'{self.first_name.capitalize()}'
        
    def index_display(self):
        if self.last_name:
            if len(self.last_name) > 7:
                return f'{(self.first_name[0].upper())}. {self.last_name[:6].capitalize()}...'
            else:
                return f'{(self.first_name[0].upper())}. {self.last_name.capitalize()}'
        else:
            if len(self.first_name) > 10:
                return f'{self.first_name[:5].capitalize()}'
            else:
                return f'{self.first_name.capitalize()}'        
    

class Room(models.Model):
    identifier = models.CharField(max_length=8)
    occupancy = models.IntegerField()

    def __str__(self):
        return self.identifier    
    

class Booking(models.Model):
    main_guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
    total_guests = models.IntegerField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    check_in = models.DateTimeField('check-in')
    check_out = models.DateTimeField('check-out')

    def __str__(self):
        return f'{self.main_guest}'

    def index(self):
        return f'{self.main_guest.index_display()}'    



    
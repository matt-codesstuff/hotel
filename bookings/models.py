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
                return f'{self.first_name[:6].capitalize()}...'
            else:
                return f'{self.first_name.capitalize()}'        
    

class Floor(models.Model):
    identifier = models.CharField(max_length=25)

    def __str__(self):
        return f'Floor {self.identifier}'


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('SNGL', 'Single'),
        ('DBL', 'Double'),
        ('TWN', 'Twin'),
        ('TRPL', 'Triple'),
        ('QUAD', 'Quad'),
        ('FML', 'Family')
    ]
    identifier = models.CharField(max_length=8)
    type = models.CharField(max_length=8, choices = ROOM_TYPE_CHOICES)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    occupancy = models.IntegerField()

    def __str__(self):
        return self.identifier


class ShopItems(models.Model):
    item = models.CharField(max_length=200)
    item_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Shop items'

    def __str__(self):
        return f'{self.item}, {self.item_amount}'


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('CSH', 'Cash'),
        ('VCC', 'Visa(CC)'),
        ('MCC', 'Mastercard(CC)'),
        ('AMEX', 'American Express'),
        ('DC', 'Debit Card')] 
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItems, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=None)
    date = models.DateTimeField('payment date', default=timezone.now)

    def __str__(self):
        return f'{self.guest}, {self.payment_amount}, {self.date}'            
    

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



    
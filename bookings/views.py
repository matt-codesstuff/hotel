from datetime import timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import Booking


def index(request, *date_check):
    booking_list = []
    dates = []
    bookings = Booking.objects.all()

    if not date_check:
        date_check = timezone.now()        

    for booking in bookings:
        if  booking.check_in <= date_check and date_check <= booking.check_out:
            booking_list.append(booking) 

    for i in range(10):
        dates.append(date_check.strftime('%d/%m/%y'))
        date_check += timedelta(days=1)         

    return render(request, 'bookings/index.html', 
                  {'booking_list': booking_list, 
                   'dates' : dates})

def detail(request, booking_id):
    return HttpResponse(f'you are viewing detalis for {booking_id} booking')
 
def new_booking(request):
    return HttpResponse('You are creating a new booking')
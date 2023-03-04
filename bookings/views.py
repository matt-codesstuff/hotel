from datetime import timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import Booking, Room

DAYCOUNT = 10


def index(request, *date_check):

    if not date_check:
        date_check = timezone.now()

    booking_list = []
    dates = ['Room',]
    rooms = Room.objects.all()
    bookings = Booking.objects.filter(check_in__range=(date_check - timedelta(days=14), date_check + timedelta(days=14)))    

    date_check_header = date_check        
    # prepare a list of dates
    for i in range(DAYCOUNT):
        dates.append(date_check_header.strftime('%d/%m/%y'))
        date_check_header += timedelta(days=1)
    # populate booking_list with a new list for each room
    for room_nr in rooms:        
        booking_list.append([room_nr])
    # populate each day of room list
    for room_row in booking_list:
        for i in range(DAYCOUNT):
            room_row.append(None)

    for row in booking_list:
        # narrow lookup to only bookings for the current room
        bookings_per_room = bookings.filter(room=row[0])
        if bookings_per_room:
            for day in row:
                for booking in bookings_per_room:
                    # reset this variable for each booking
                    date_check_booking = date_check
                    for i , j in enumerate(range(DAYCOUNT), 1):
                        if booking.check_in <= date_check_booking <=booking.check_out:
                            row[i] = booking
                            date_check_booking += timedelta(days=1)
                        else:
                            date_check_booking += timedelta(days=1)                   

    return render(request, 'bookings/index.html', 
                  {'booking_list': booking_list, 
                   'dates' : dates,
                   'bookings': bookings,
                   'bookings_per_room': bookings_per_room,})          

            
def detail(request, booking_id):
    return HttpResponse(f'you are viewing detalis for {booking_id} booking')
 
def new_booking(request):
    return HttpResponse('You are creating a new booking')
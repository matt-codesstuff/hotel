import pytz

from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Booking, Room, Guest
from .forms import NewBookingForm

DAYCOUNT = 10
AMSTERDAM = pytz.timezone('Europe/Amsterdam')

def index(request):
    # get date from POST request and add tzinfo so all date objects in this view are aware
    if request.method == 'POST':
        date = request.POST.get('date')       
        date_check = datetime.fromisoformat(date).replace(tzinfo=AMSTERDAM)                
    else:
        date_check = timezone.now()

    booking_list = []
    dates = ['Room']
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
    # populate each day of room list with datetime objects converted to string for easy passing through urlconfig
    for room_row in booking_list:
        d = date_check
        for i in range(DAYCOUNT):
            room_row.append(d.strftime('%d%m%y'))
            d += timedelta(days=1)
           
    for row in booking_list:
        # narrow lookup to only bookings for the current room
        bookings_per_room = bookings.filter(room=row[0])
        if bookings_per_room:
            for day in row:
                for booking in bookings_per_room:
                    # reset this variable for each booking
                    date_check_booking = date_check
                    for i , j in enumerate(range(DAYCOUNT), 1):
                        # check each date to see if booking falls on that day, and write the booking in to 
                        # the current date if it does
                        if booking.check_in <= date_check_booking <= booking.check_out:
                            row[i] = booking
                            date_check_booking += timedelta(days=1)
                        else:
                            date_check_booking += timedelta(days=1)                   

    return render(request, 'bookings/index.html', 
                  {'booking_list': booking_list, 
                   'dates' : dates,})       

            
def detail(request, booking_id):
    return HttpResponse(f'you are viewing details for booking {booking_id}')
 
def new_booking(request, room_id, date):
    if request.method == 'POST':
        form = NewBookingForm(request.POST)
        
        if form.is_valid():
            first = request.POST.get('first_name')
            last = request.POST.get('last_name')
            room_nr = request.POST.get('room')
            total_guests = request.POST.get('total_guests')
            rate = request.POST.get('rate')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')

            room = Room.objects.get(identifier=room_nr)
                
            g = Guest(first_name = first, 
                          last_name = last)
            g.save()
                
            b = Booking(main_guest = g,
                            room = room,
                            rate = rate,
                            total_guests = total_guests,
                            check_in = check_in,
                            check_out = check_out)
            b.save()

            return redirect('bookings:index')
        else:
            return HttpResponse("You done ffed up")
    else:        
        room = Room.objects.get(pk=room_id)
        day = date[:2]
        month = date[2:4]
        year = date[4:]
        co_day = str(int(day) + 1)
        co = co_day + month + year

        check_in = datetime.strptime(date, '%d%m%y')
        check_out = datetime.strptime(co, '%d%m%y')

        data = {'check_in': check_in,
                    'check_out': check_out,
                    'room': room}
        form = NewBookingForm(initial=data)

    return render(request, 'bookings/new_booking.html',
                    {'form': form,
                    'room': room,})



        



   

import pytz

from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Booking, Room, Guest, Floor, ShopItems
from .forms import NewBookingForm, DatePickerForm, ShopForm, ItemForm, PaymentForm

DAYCOUNT = 10
AMSTERDAM = pytz.timezone('Europe/Amsterdam')
TALLY_LIST = []


def index(request):
    # get the starting date for the table displayed on the index page.
    # if no date is given, set the date to timezone.now
    # if the date is given, make a datetime object from it and add timezone data
    if request.method == 'POST':
        date = request.POST.get('date')       
        date_check = datetime.fromisoformat(date).replace(tzinfo=AMSTERDAM)                
    else:
        date_check = timezone.now()

    form = DatePickerForm(initial={'date': date_check})        

    # set up lists and variables 
    dates = ['Room']
    rooms = Room.objects.all()
    floors = Floor.objects.all()
    bookings = Booking.objects.filter(check_in__range=(date_check - timedelta(days=14), date_check + timedelta(days=14)))
    floor_dict = dict.fromkeys(floors)    
    date_check_header = date_check

    # set up initial table. firstly, create a list of dates to be displayed in table header for each floor 
    for i in range(DAYCOUNT):
        dates.append(date_check_header.strftime('%d/%m/%y'))
        date_check_header += timedelta(days=1)
    # for each floor, create a 2d array cosisting of a list that contains lists for each room on that floor, then add to dictionary
    for floor in floor_dict:
        bookings_per_floor = []
        rooms_per_floor = rooms.filter(floor=floor)
        for room_nr in rooms_per_floor:        
            bookings_per_floor.append([room_nr])
        floor_dict[floor] = bookings_per_floor
    # then populate each room list with datetime objects to the amount of the DAYCOUNT value
    # each datetime object gets converted to string, removing any slashes. this makes it easier to pass through urlconfig later on
    for floor in floor_dict:
        for room_row in floor_dict[floor]:
            d = date_check
            for i in range(DAYCOUNT):
                room_row.append(d.strftime('%d%m%y'))
                d += timedelta(days=1)

    #fill the table with bookings
    for floor in floor_dict:      
        for row in floor_dict[floor]:
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
                  { 'dates' : dates,
                   'floor_dict': floor_dict,
                   'form': form})       

            
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
            check_in = datetime.fromisoformat(request.POST.get('check_in')).replace(tzinfo=AMSTERDAM)
            check_out = datetime.fromisoformat(request.POST.get('check_out')).replace(tzinfo=AMSTERDAM)
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
            return HttpResponse("Something went wrong.")
    else:        
        room = Room.objects.get(pk=room_id)
        check_in = datetime.strptime(date, '%d%m%y')
        check_out = check_in 
        check_out += timedelta(days=1)

        data = {'check_in': check_in,
                    'check_out': check_out,
                    'room': room}
        form = NewBookingForm(initial=data)

    return render(request, 'bookings/new_booking.html',
                    {'form': form,
                    'room': room,})

def shop(request):
    total_due = 0
    item_form_list = []
    payment_form = PaymentForm()
    

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid:
            item = request.POST.get('item')
            item_model = ShopItems.objects.get(pk=item)
            TALLY_LIST.append(item_model)
            form = ShopForm(initial={'tally': TALLY_LIST})            
    else:        
        form = ShopForm()

    for item in TALLY_LIST:
        total_due += item.item_amount
        item_form_list.append(ItemForm(initial={'item': item}))    
    
    return render(request, 'bookings/shop.html',
                  {'form': form,
                   'tally_list': TALLY_LIST,
                   'total_due': total_due,
                   'item_form_list': item_form_list,
                   'payment_form': payment_form})

def delete_store_item(request, item_id):
    del_item = ShopItems.objects.get(pk=item_id)
    TALLY_LIST.remove(del_item)
    return redirect('bookings:shop')




        



   

from django import forms
from bookings.models import Guest, Booking





        


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50)
    rate = forms.DecimalField(max_digits=6, decimal_places=2)
    check_in = forms.DateTimeField(widget=DateInput())
    check_out = forms.DateTimeField(widget=DateInput())



    
from django import forms
from bookings.models import Guest, Booking, Room


class DateInput(forms.DateInput):
    input_type = 'date' 


class NewBookingForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    rate = forms.DecimalField(max_digits=6, decimal_places=2)
    room = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    total_guests = forms.IntegerField()
    check_in = forms.DateTimeField(widget=DateInput(attrs={'readonly': True}),required=False)
    check_out = forms.DateTimeField(widget=DateInput())

    
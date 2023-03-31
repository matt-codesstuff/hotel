from django import forms
from bookings.models import Payment, Guest, ShopItems


class DateInput(forms.DateInput):
    input_type = 'date' 


class ItemChoice(forms.Select):
    input_type = 'select'    


class NewBookingForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    rate = forms.DecimalField(max_digits=6, decimal_places=2)
    room = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    total_guests = forms.IntegerField()
    check_in = forms.DateTimeField(widget=DateInput(attrs={'readonly': True}),required=False)
    check_out = forms.DateTimeField(widget=DateInput())


class DatePickerForm(forms.Form):
    date = forms.DateField(widget=DateInput(), label='') 


class ShopForm(forms.Form):       
    guest = forms.ModelChoiceField(queryset=Guest.objects.all().order_by('last_name'))
    item = forms.ModelChoiceField(queryset=ShopItems.objects.all().order_by('item'), widget=forms.Select(attrs={'onchange': 'this.form.submit()'}))


class ItemForm(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'style': 'border:none'}), label='')


   
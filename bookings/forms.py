from django import forms


class DateForm(forms.Form):
    date = forms.DateTimeField()
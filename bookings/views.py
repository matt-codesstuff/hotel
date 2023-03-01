from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('hello world!')

def detail(request, booking_id):
    return HttpResponse(f'you are viewing detalis for {booking_id} booking')

def new_booking(request):
    return HttpResponse('You are creating a new booking')
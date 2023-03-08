from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:booking_id>/', views.detail, name='detail'),
    path('new_booking', views.new_booking, name='new_booking'),
]

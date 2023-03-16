from django.urls import path, re_path
from . import views


app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:booking_id>/', views.detail, name='detail'),
    path('new_booking/<int:room_id>/<str:date>', views.new_booking, name='new_booking'),
]

from django.urls import path, register_converter
from datetime import datetime
from . import views

class DateConverter:
    regex = '\d{2}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    #path('index', views.index, name='index'),
    path('<int:booking_id>/', views.detail, name='detail'),
    path('new', views.new_booking, name='new_booking'),
]

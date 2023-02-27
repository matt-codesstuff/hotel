from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:booking_id>', views.detail, name='detail'),
    path('new', views.new_booking, name='new_booking'),
]

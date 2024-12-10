from django.urls import path

from .views import booking_calendar_view, BookingCreateView, create_booking, get_bookings

app_name = 'audioconf'

urlpatterns = [
    path('', booking_calendar_view, name='index'),
    path('create/', create_booking, name='create-booking'),
    path('get-bookings/', get_bookings, name='get-bookings'),
]

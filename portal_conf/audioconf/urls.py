from django.urls import path

from .views import (booking_calendar_view, create_booking, get_bookings,
                    AcsPhoneListView, AcsPhoneDetail)

app_name = 'audioconf'

urlpatterns = [
    path('', booking_calendar_view, name='index'),
    path('create/', create_booking, name='create_booking'),
    path('get-bookings/', get_bookings, name='get_bookings'),
    path('acs-phones/', AcsPhoneListView.as_view(), name='phones_list'),
    path('acs-phone/<int:pk>/', AcsPhoneDetail.as_view(), name='phone_detail')
]

from django.urls import path

from .views import booking_calendar_view

app_name = 'audioconf'

urlpatterns = [
    path('', booking_calendar_view, name='index')
]

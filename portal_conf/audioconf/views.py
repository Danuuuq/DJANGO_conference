from django.shortcuts import render
from django.views.generic import (
    DetailView, ListView, UpdateView, CreateView)

from .models import AcsPhone, BookingAcs


def booking_calendar_view(request):
    # Получаем все бронирования для отображения
    bookings = BookingAcs.objects.select_related('acs_phone', 'owner')
    
    # Преобразуем данные для календаря
    events = []
    for booking in bookings:
        events.append({
            'title': f'Бронь: {booking.acs_phone.phone}',
            'start': booking.start_conf.isoformat(),
            'end': booking.end_conf.isoformat(),
            'owner': booking.owner.username,  # Информация о владельце
        })
    
    context = {
        'events': events,
    }
    
    return render(request, 'conference/index.html', context)


# class BookingListView(ListView):
#     model = BookingAcs
#     queryset = BookingAcs.objects.with_related_data()
#     template_name = 'conference/booking_calendar.html'

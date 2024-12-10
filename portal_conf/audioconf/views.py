
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .models import BookingAcs, AcsPhone
from .forms import BookingForm


def booking_calendar_view(request):
    bookings = BookingAcs.objects.with_related_data()
    acs_phones = AcsPhone.objects.all()

    events = []
    for booking in bookings:
        events.append({
            'title': f'{booking.acs_phone.phone} - {booking.owner.username}',
            'start': booking.start_conf.isoformat(),
            'end': booking.end_conf.isoformat(),
            'owner': booking.owner.username,
        })

    context = {
        'events': events,
        'acs_phones': acs_phones
    }

    return render(request, 'conference/index.html', context)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = BookingAcs
    form_class = BookingForm
    template_name = 'booking_form.html'  # Форма для отображения

    def form_valid(self, form):
        # Устанавливаем владельца как текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('calendar-view')

@login_required
@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        acs_phone_id = request.POST.get('acs_phone')
        start_conf = parse_datetime(request.POST.get('start_conf'))
        end_conf = parse_datetime(request.POST.get('end_conf'))

        # Валидация и создание бронирования
        if start_conf and end_conf:
            booking = BookingAcs.objects.create(
                acs_phone_id=acs_phone_id,
                start_conf=start_conf,
                end_conf=end_conf,
                owner=request.user
            )
            return JsonResponse({'status': 'success', 'booking_id': booking.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)


def get_bookings(request):
    bookings = BookingAcs.objects.all()
    events = []
    for booking in bookings:
        events.append({
            'title': str(booking.acs_phone),
            'start': booking.start_conf.isoformat(),
            'end': booking.end_conf.isoformat(),
        })
    return JsonResponse(events, safe=False)
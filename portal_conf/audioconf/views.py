import datetime as dt 

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime

from .models import BookingAcs, AcsPhone
from .forms import BookingForm


def booking_calendar_view(request):
    bookings = BookingAcs.objects.with_related_data()
    acs_phones = AcsPhone.objects.all()

    events = []
    for booking in bookings:
        events.append({
            'title': f'{booking.acs_phone.phone} - {booking.responsible}',
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
    template_name = 'booking_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('calendar-view')


@login_required
@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.save()
            acs_phone = AcsPhone.objects.get(id=request.POST.get('acs_phone'))
            return JsonResponse({'status': 'success',
                                 'message': 'Бронирование успешно создано',
                                 'acs_phone': str(acs_phone.phone),
                                 'pin_code': str(acs_phone.password)})
        else:
            return JsonResponse({'status': 'error', 'error': form.errors},
                                status=400)
    return JsonResponse({'status': 'error',
                         'message': 'Only POST requests are allowed'},
                        status=405)


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


class AcsPhoneListView(ListView):
    model = AcsPhone
    queryset = AcsPhone.objects.with_related_data()
    ordering = 'phone'
    template_name = 'conference/acs_phone_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(phone__icontains=search_query) |
                Q(department__employees__last_name__icontains=search_query) |
                Q(department__name__icontains=search_query)
            )
        return queryset


class AcsPhoneDetail(DetailView):
    model = AcsPhone
    template_name = 'conference/acs_phone_detail.html'
    context_object_name = 'acs_phone'
    queryset = AcsPhone.objects.with_related_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = (
            self.object.bookings.all().filter(start_conf__gte=dt.datetime.now())
        )
        context['employees'] = (
            self.object.department.employees.all()
        )
        return context

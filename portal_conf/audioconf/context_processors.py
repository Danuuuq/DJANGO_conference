from .forms import BookingForm


def booking_form(request):
    return {'appointment_form': BookingForm}

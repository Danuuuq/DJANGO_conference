from django import forms
from .models import BookingAcs, User


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingAcs
        fields = ['acs_phone', 'start_conf', 'end_conf', 'responsible']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username'
        )

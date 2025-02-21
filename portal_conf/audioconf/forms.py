from django import forms
from .models import BookingAcs, User


class BookingForm(forms.ModelForm):

    def clean_record(self):
        if self.cleaned_data.get('record'):
            return True
        return False

    class Meta:
        model = BookingAcs
        fields = ['acs_phone', 'start_conf', 'end_conf',
                  'responsible', 'record']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username'
        )

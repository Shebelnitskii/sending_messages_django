from django import forms
from django.forms import TimeInput, DateInput
from main.models import Message, Client


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['client', 'letter_subject', 'letter_body', 'mailing_time', 'periodicity']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


def validate_time(value):
    try:
        forms.TimeField().clean(value)
    except forms.ValidationError:
        raise forms.ValidationError('Некорректное время')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'first_name']

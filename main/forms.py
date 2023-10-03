from django import forms
from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment', 'is_active']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['time_to_send', 'end_time', 'frequency', 'status', 'recipients']
        widgets = {
            'recipients': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipients'].queryset = user.client_set.all()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

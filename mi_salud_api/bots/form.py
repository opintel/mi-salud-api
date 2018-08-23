from secrets import token_urlsafe
from django import forms
from .models import Bot


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = [
            'name',
            'token',
            'enable'
        ]

    def __init__(self, *args, **kwargs):
        if not kwargs.get('initial') and not kwargs.get('instance'):
            kwargs['initial'] = {}
            kwargs['initial'].update({'token': token_urlsafe(16)})

        super(BotForm, self).__init__(*args, **kwargs)

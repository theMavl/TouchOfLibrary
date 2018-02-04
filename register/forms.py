import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from register.models import DocumentInstance


class OrderDocument(forms.Form):
    due_date = forms.DateField(help_text="Enter a date between now and 2 weeks.")

    def clean_due_date(self):
        data = self.cleaned_data['due_date']

        # If date from the past
        if data < datetime.date.today():
            raise ValidationError('Wrong date - date from the past')

        # If the interval is bigger than 2 weeks
        if data > datetime.date.today() + datetime.timedelta(14):
            raise ValidationError('You cannot take it for more than 2 weeks')

        return data

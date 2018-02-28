import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from library.models import DocumentInstance


class DueDateForm(forms.Form):

    due_date = forms.DateField(help_text="Enter a date when the document must be returned.")
    max_days = 1

    def clean_due_date(self):
        data = self.cleaned_data['due_date']
        # If date from the past
        if data < datetime.date.today():
            raise ValidationError('Wrong date - date from the past')

        # If the interval is bigger than 2 weeks
        if data > datetime.date.today() + datetime.timedelta(self.max_days):
            raise ValidationError('Wrong date - out of limit borders')

        return data

class MyForm(forms.ModelForm):
    class Meta:
        model = DocumentInstance
        fields = '__all__'

import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from library.models import DocumentInstance


class ReserveButton(forms.Form):
    def clean_order(self):
        order = False
        if 'cancel_order' in self.data:
            order = False
        elif 'document_order' in self.data:
            order = True
        return order


class CheckOutButton(forms.Form):
    def clean_check_out(self):
        checkOut = False
        if 'deny_order' in self.data:
            checkOut = False
        elif 'accept_order' in self.data:
            checkOut = True
        return checkOut

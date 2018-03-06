import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import PatronType
from django.forms import ModelForm
from django.contrib.auth.models import User

from library.models import DocumentInstance, Author, DocType


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


class ReturnDocumentForm(forms.Form):
    librarian_confirmation = forms.BooleanField()

    def confirmed(self):
        librarian_confirm = self.cleaned_data['librarian_confirm']

        if not librarian_confirm:
            raise ValidationError('You must confirm the return')


class DocumentInstanceUpdate(forms.ModelForm):
    class Meta:
        model = DocumentInstance
        fields = 'status', 'location', 'price', 'additional_field1', 'additional_field2', 'additional_field3', 'additional_field4', 'additional_field5'


class DocumentInstanceDelete(forms.ModelForm):
    class Meta:
        model = DocumentInstance
        fields = '__all__'


class DocumentInstanceCreate(forms.ModelForm):
    class Meta:
        model = DocumentInstance
        fields = 'status', 'location', 'price', 'additional_field1', 'additional_field2', 'additional_field3', 'additional_field4', 'additional_field5'


class AddPatron(forms.Form):
    username = forms.CharField(label="Login", max_length=20, required=True)
    name = forms.CharField(max_length=20, required=True)
    surname = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    telegram = forms.CharField(required=False)

    type = forms.ModelChoiceField(label="Patron Group", queryset=PatronType.objects.all())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('The username already exist')
        return username

    def clean_name(self):
        data = self.cleaned_data['name']

        if not (str(data).istitle()):
            raise ValidationError('Name should starts with Upper Case letter')

        if not (str(data).isalpha()):
            raise ValidationError('Name should consist only letters')

        return data

    def clean_surname(self):
        data = self.cleaned_data['surname']

        if not (str(data).istitle()):
            raise ValidationError('Surname should starts with Upper Case letter')

        if not (str(data).isalpha()):
            raise ValidationError('Surname should consist only letters')

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        validate_email(data)
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not str(data).isdigit():
            raise ValidationError('Phone Number must consist only by numbers')

        return data

    def clean_telegram(self):
        data = self.cleaned_data['telegram']
        if not str(data).startswith("@"):
            raise ValidationError('Telegram alias must starts with "@" symbol')

        return data


class EditPatron(forms.Form):
    username = forms.CharField(label="Login", max_length=20, required=False, disabled=True)
    name = forms.CharField(max_length=20, required=True)
    surname = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(max_length=200, required=True)
    telegram = forms.CharField(required=False)

    type = forms.ModelChoiceField(label="Patron Group: ", queryset=PatronType.objects.all())

    def clean_name(self):
        data = self.cleaned_data['name']

        if not (str(data).istitle()):
            raise ValidationError('Name should starts with Upper Case letter')

        if not (str(data).isalpha()):
            raise ValidationError('Name should consist only letters')

        return data

    def clean_surname(self):
        data = self.cleaned_data['surname']

        if not (str(data).istitle()):
            raise ValidationError('Surname should starts with Upper Case letter')

        if not (str(data).isalpha()):
            raise ValidationError('Surname should consist only letters')

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        validate_email(data)
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not str(data).isdigit():
            raise ValidationError('Phone Number must consist only by numbers')

        return data

    def clean_telegram(self):
        data = self.cleaned_data['telegram']
        if not str(data).startswith("@"):
            raise ValidationError('Telegram alias must starts with "@" symbol')

        return data


class DeletePatron(forms.Form):
    comment = forms.CharField(max_length=30, required=False)


class AuthorUpdate(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorDelete(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorCreate(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class TypeCreate(forms.ModelForm):
    class Meta:
        model = DocType
        fields = '__all__'


class TypeUpdate(forms.ModelForm):
    class Meta:
        model = DocType
        fields = '__all__'


class TypeDelete(forms.ModelForm):
    class Meta:
        model = DocType
        fields = '__all__'

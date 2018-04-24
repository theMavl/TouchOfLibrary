import datetime

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from library.models import User, DocumentInstance, Author, DocType, Tag, Document, LibraryLocation
from .models import PatronType

from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib


class DueDateForm(forms.Form):
    due_date = forms.DateField()
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


class RenewDocumentForm(forms.Form):
    due_date = forms.DateField(help_text="Enter the date for renewal")
    max_days = 1
    error_outstanding_request = False
    error_limit_of_renewals = False
    return_date = None

    def clean_due_date(self):
        data = self.cleaned_data['due_date']
        # If date from the past
        if data < self.return_date:
            raise ValidationError('Wrong date - date before the return')

        # If the interval is out of limit
        if data > self.return_date + datetime.timedelta(self.max_days):
            raise ValidationError('Wrong date - out of limit borders')

        if self.error_outstanding_request:
            raise ValidationError('Can not renew - there is an outstanding request for this book')

        if self.error_limit_of_renewals:
            raise ValidationError('Can not renew - reached the limit of renewals')

        return data


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
        if not str(data).startswith("@") and not len(str(data)) == 0:
            raise ValidationError('Telegram alias must starts with "@" symbol')

        return data


class EditUserPerms(forms.Form):
    groups = forms.ModelMultipleChoiceField(label="User group", queryset=Group.objects.all(), required=False)


class EditPatron(forms.Form):
    username = forms.CharField(label="Login", max_length=20, required=False, disabled=True)
    name = forms.CharField(max_length=20, required=True)
    surname = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(max_length=200, required=True)
    telegram = forms.CharField(required=False)
    is_limited = forms.BooleanField(help_text="Limited users can not reserve, request and check-out books",
                                    required=False)
    is_patron = forms.BooleanField(help_text="Determines whether user is patron or just user",
                                   required=False)
    type = forms.ModelChoiceField(label="Patron Group", queryset=PatronType.objects.all())

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
        if not str(data).startswith("@") and not str(data) == "None":
            raise ValidationError('Telegram alias must starts with "@" symbol')

        return data


class RequestAllConfirm(forms.Form):
    librarian_confirmation = forms.BooleanField(
        help_text="You need to confirm deletion. You will not be able to undo requests!",
        required=True)
    reason = forms.CharField(label="Reason", max_length=50, required=True)


class DeletePatron(forms.Form):
    reason = forms.CharField(max_length=30, required=True)
    librarian_confirmation = forms.BooleanField()


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


class LocationCreate(forms.ModelForm):
    class Meta:
        model = LibraryLocation
        fields = '__all__'


class LocationUpdate(forms.ModelForm):
    class Meta:
        model = LibraryLocation
        fields = '__all__'


class LocationDelete(forms.ModelForm):
    class Meta:
        model = LibraryLocation
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


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    telegram = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address',
            'telegram')


class TagCreate(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TagUpdate(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TagDelete(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class DocImageForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class ImageDirectForm(DocImageForm):
    image = CloudinaryJsFileField()


class ImageUnsignedDirectForm(DocImageForm):
    upload_preset_name = "sample_" + hashlib.sha1(
        to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)

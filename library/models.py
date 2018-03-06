from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Q


class Document(models.Model):
    """
    Model of abstract document
    """
    # document attributes
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author', help_text='Select authors')
    description = models.TextField(max_length=1000, help_text="Enter a description of the document")
    type = models.ForeignKey('DocType', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', help_text="Select tags")
    last_quantity = models.IntegerField(
        help_text='This field is used for storing quantity after recalculation. DO NOT USE IT, use quantity() instead!',
        null=True)
    bestseller = models.BooleanField(default=False)
    quantity_synced = models.BooleanField(default=False)
    is_reference = models.BooleanField(default=False, help_text="Reference materials can not be borrowed.")

    def quantity(self) -> int:
        if not self.quantity_synced:
            n = len(DocumentInstance.objects.filter(document_id=self.id, status='a'))
            self.last_quantity = n
            self.quantity_synced = True
            self.save()
        else:
            n = self.last_quantity
        return n

    def quantity_real(self):
        return len(DocumentInstance.objects.filter(Q(document_id=self.id) & (Q(status='a') | Q(status='r'))))

    def str_authors(self):
        authors_list = [str(x) for x in list(self.authors.all())]
        return ', '.join(authors_list)

    # document features
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-detail', args=[str(self.id)])


class DocumentInstance(models.Model):
    """
        Model of real document in the library
    """
    # instance attributes
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique document ID")
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True)
    due_back = models.DateField(null=True, blank=True)

    DOCUMENT_STATUS = (
        ('a', 'Available'),
        ('g', 'Given out'),
        ('r', 'Reserved'),
        ('m', 'Maintenance')
    )

    status = models.CharField(max_length=1, choices=DOCUMENT_STATUS, blank=True, default='d')

    location = models.ForeignKey('LibraryLocation', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField(help_text='Price in RUB', null=True)
    holder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    additional_field1 = models.CharField(max_length=500, blank=True)
    additional_field2 = models.CharField(max_length=500, blank=True)
    additional_field3 = models.CharField(max_length=500, blank=True)
    additional_field4 = models.CharField(max_length=500, blank=True)
    additional_field5 = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["due_back"]

    def form_return_request_mail(self):
        n_line = "%0A%0A"
        message = "mailto:%s?subject=Return document to Library&body=Dear %s %s,%sThis is Touch of Library. " \
               "Please return %s to the library as soon as possible." \
               "%sRegards,%sTouch of Library." % (
                   self.holder.email, self.holder.first_name, self.holder.last_name, n_line, self.summary(), n_line,
                   n_line[:3])
        print(message)
        return message

    def summary(self):
        fields = [self.additional_field1, self.additional_field2,
                  self.additional_field3, self.additional_field4, self.additional_field5]
        fields_str = ', '.join([x for x in fields if x != ""])
        return '%s %s "%s" (%s)' % (str(self.document.type).lower(),
                                    self.document.str_authors(), self.document.title, fields_str)

    @property
    def is_overdue(self):
        if self.due_back is None:
            return False
        if datetime.date.today() > self.due_back:
            return True
        else:
            return False

    # instance attributes
    def __str__(self):
        return '%s (%s)' % (self.document.title, self.id)

    def get_absolute_url(self):
        return reverse('document-detail', args=[str(self.document.id)])


class Author(models.Model):
    """
    Model of author
    """

    # Author attributes
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_born = models.DateField(null=True, blank=True)
    date_died = models.DateField('Died', null=True, blank=True)

    # Author features
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s. %s' % (self.first_name[0], self.last_name)


class LibraryLocation(models.Model):
    """
        Location of each document instance
    """
    room = models.IntegerField(help_text='Room in library', null=True)
    level = models.IntegerField(help_text='Level in library', null=True)

    def __str__(self):
        return '%d-%d' % (self.level, self.room)


class DocType(models.Model):
    name = models.CharField(max_length=50, help_text="Document type name")
    fields = models.CharField(max_length=1000, blank=True,
                              help_text="Fields labels separated with semicolon. Max: 5")
    max_days = models.IntegerField(help_text='Maximum days for loan in regular case', null=True)
    max_days_bestseller = models.IntegerField(help_text='Maximum days for loan if document is bestseller', null=True)
    max_days_privileges = models.IntegerField(help_text='Maximum days for loan for privileged patrons', null=True)

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Documents' Types"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('types-detail', args=[str(self.id)])


class PatronInfo(models.Model):
    """
        Model of patron
    """
    # Patron attributes
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    telegram = models.CharField(max_length=20, blank=True)
    patron_type = models.ForeignKey('PatronType', on_delete=models.SET_NULL, null=True)

    # Patron features
    def get_name(self):
        return "kek"

    def form_mail_about_deletion(self):
        n_line = "%0A%0A"
        return "mailto:%s?subject=The deletion of your account in Library&body=Dear %s %s,%sThis is Touch of Library. " \
               "We inform you that your account has been deleted." \
               "%sReason:" \
               "%sRegards,%sTouch of Library." % (
                   self.user.email, self.user.first_name, self.user.last_name, n_line, n_line, n_line,
                   n_line[:3])

    class Meta:
        verbose_name = "Patron's Information"
        verbose_name_plural = "Patrons' Information"

    def get_absolute_url(self):
        return reverse('patron-details', args=[str(self.user_id)])

    def __str__(self):
        return '[%d] %s %s (%s), %s, %s, TG: %s' % (
        self.user.id, self.user.first_name, self.user.last_name, self.patron_type, self.phone_number, self.address,
        self.telegram)


class PatronType(models.Model):
    title = models.CharField(max_length=100, blank=True)
    # max_days = models.IntegerField(help_text='Maximum number of days allowed', null=True)
    max_documents = models.IntegerField(help_text='Maximum number of days allowed', null=True)
    privileges = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GiveOut(models.Model):
    """
        Model of giving-out a document to an user
    """
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=True)
    patron = models.ForeignKey('PatronInfo', on_delete=models.PROTECT, null=True)
    document = models.ForeignKey('Document', on_delete=models.PROTECT, null=True)
    document_instance = models.ForeignKey('DocumentInstance', on_delete=models.PROTECT, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('document_instance__due_back', )

    @property
    def is_overdue(self):
        return self.document_instance.is_overdue

    def get_absolute_url(self):
        return reverse('return-document', args=[str(self.id)])


class Reservation(models.Model):
    """
        Model of reservation on a book
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True)
    document_copy = models.ForeignKey('DocumentInstance', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    executed = models.BooleanField(default=False)

    @staticmethod
    def clean_old_reservations():
        orders = [x for x in Reservation.objects.all() if x.is_old]
        n = len(orders)
        for x in orders:
            x.document.quantity_synced = False
            x.document.save()
            if x.document_copy is not None:
                x.document_copy.status = 'a'
                x.document_copy.save()
            x.delete()
        return n

    @property
    def is_old(self):
        if datetime.date.today() > self.timestamp.date() + datetime.timedelta(days=5):
            return True
        return False

    def due_date(self):
        return str(self.timestamp.date() + datetime.timedelta(days=5))


class Tag(models.Model):
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('tags-detail', args=[str(self.id)])

    def create_url(self):
        return reverse('tag-create')

    def edit_url(self):
        return reverse('tag-update', args=[str(self.id)])

    def delete_url(self):
        return reverse('tag-deleteconfirm', args=[str(self.id)])


class GiveOutLogEntry(models.Model):
    timestamp_given_out = models.DateTimeField()
    timestamp_due_back = models.DateTimeField()
    timestamp_returned = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    patron_information = models.CharField(max_length=200)
    document_instance_summary = models.CharField(max_length=200)

    def is_overdue(self):
        if self.timestamp_due_back.date() < self.timestamp_returned.date():
            return True
        return False

    def __str__(self):
        return "[" + str(self.timestamp_given_out.date()) + " - " + str(self.timestamp_returned.date()) + "] " + str(
            self.patron_information) + " | " + str(self.document_instance_summary)

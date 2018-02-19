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

    # instance attributes
    def __str__(self):
        return '%s (%s)' % (self.document.title, self.id)


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
        return '%s, %s' % (self.last_name, self.first_name)


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


class PatronInfo(models.Model):
    """
        Model of patron
    """
    # Patron attributes
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    telegram = models.CharField(max_length=20, blank=True)
    patron_type = models.ForeignKey('PatronType', on_delete=models.SET_NULL, null=True)

    # Patron features
    def get_name(self):
        return "kek"

    class Meta:
        verbose_name = "Patron's Information"
        verbose_name_plural = "Patrons' Information"

    def __str__(self):
        return '[%d] %s %s' % (self.user.id, self.user.first_name, self.user.last_name)


class PatronType(models.Model):
    title = models.CharField(max_length=100, blank=True)
    # max_days = models.IntegerField(help_text='Maximum number of days allowed', null=True)
    max_documents = models.IntegerField(help_text='Maximum number of days allowed', null=True)
    privileges = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RecordsLog(models.Model):
    """
        Model of each record about each check out
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey('Document', on_delete=models.PROTECT, null=True)
    document_instance = models.ForeignKey('DocumentInstance', on_delete=models.PROTECT, null=True)
    ACTION_DIRECTION = (
        (0, 'received'),
        (1, 'returned')
    )
    action = models.IntegerField(choices=ACTION_DIRECTION)
    timestamp = models.DateTimeField(auto_now=True)


class WishList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True)
    document_copy = models.ForeignKey('DocumentInstance', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    executed = models.BooleanField(default=False)

    @staticmethod
    def clean_old_wishes():
        orders = [x for x in WishList.objects.all() if x.is_old]
        n = len(orders)
        for x in orders:
            x.document.quantity_synced = False
            x.document_copy.status = 'a'
            x.document.save()
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

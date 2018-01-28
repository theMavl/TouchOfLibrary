from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author', help_text='Select authors')
    description = models.TextField(max_length=1000, help_text="Enter a description of the document")
    type = models.ForeignKey('DocType', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-detail', args=[str(self.id)])


class DocumentInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique document ID")
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True)
    due_back = models.DateField(null=True, blank=True)

    is_reference = models.BooleanField(default=False, help_text="Reference materials can not be borrowed.")

    DOCUMENT_STATUS = (
        ('a', 'Available'),
        ('g', 'Given out'),
        ('r', 'Reserved'),
        ('m', 'Maintenance')
    )

    status = models.CharField(max_length=1, choices=DOCUMENT_STATUS, blank=True, default='d')

    location = models.ForeignKey('LibraryLocation', on_delete=models.SET_NULL, null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    additional_field1 = models.CharField(max_length=500, blank=True)
    additional_field2 = models.CharField(max_length=500, blank=True)
    additional_field3 = models.CharField(max_length=500, blank=True)
    additional_field4 = models.CharField(max_length=500, blank=True)
    additional_field5 = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '%s (%s)' % (self.document.title, self.id)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_born = models.DateField(null=True, blank=True)
    date_died = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class LibraryLocation(models.Model):
    room = models.IntegerField(help_text='Room in library', null=True)
    level = models.IntegerField(help_text='Level in library', null=True)

    def __str__(self):
        return '%d-%d' % (self.level, self.room)


class DocType(models.Model):
    name = models.CharField(max_length=50, help_text="Document type name")
    fields = models.CharField(max_length=1000, blank=True,
                              help_text="Fields labels separated with semicolon. Max: 5")

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Documents' Types"

    def __str__(self):
        return self.name


class PatronInfo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    telegram = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Patron's Information"
        verbose_name_plural = "Patrons' Information"

    def __str__(self):
        return '[%d] %s %s' % (self.user.id, self.user.first_name, self.user.last_name)


class RecordsLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey('DocumentInstance', on_delete=models.PROTECT, null=True)
    ACTION_DIRECTION = (
        (0, 'borrowed'),
        (1, 'returned')
    )
    action = models.IntegerField(choices=ACTION_DIRECTION)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s (%s)' % (
            self.user.first_name, self.user.last_name,
            self.ACTION_DIRECTION.__getitem__(self.action), self.document.id,
            self.document.document.title)


class Tag(models.Model):
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption

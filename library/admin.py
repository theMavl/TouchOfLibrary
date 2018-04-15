from django.contrib import admin
from .models import User, Author, Document, DocumentInstance, DocType, LibraryLocation, Tag, GiveOut, PatronType, \
    Reservation, GiveOutLogEntry, DocumentRequest

admin.site.register(User)

admin.site.register(PatronType)

admin.site.register(Author)
admin.site.register(Document)
admin.site.register(DocumentInstance)

admin.site.register(DocType)
admin.site.register(Tag)
admin.site.register(LibraryLocation)

admin.site.register(GiveOut)
admin.site.register(Reservation)
admin.site.register(GiveOutLogEntry)
admin.site.register(DocumentRequest)
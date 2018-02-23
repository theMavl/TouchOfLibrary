from django.contrib import admin
from .models import Author, Document, DocumentInstance, DocType, LibraryLocation, PatronInfo, Tag, GiveOut, PatronType, Reservation

admin.site.register(PatronInfo)
admin.site.register(PatronType)

admin.site.register(Author)
admin.site.register(Document)
admin.site.register(DocumentInstance)

admin.site.register(DocType)
admin.site.register(Tag)
admin.site.register(LibraryLocation)

admin.site.register(GiveOut)
admin.site.register(Reservation)
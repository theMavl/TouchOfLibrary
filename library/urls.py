from django.conf.urls import url

from library.forms import AuthorDelete
from library.views import *

# Maintenance routines
from library.models import Reservation
from library.views.author import author_create, author_delete
from library.views.author.author_delete import author_deleteconfirm
from library.views.author.author_update import author_update

try:
    Reservation.clean_old_reservations()
except:
    pass

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^dashboard/$', dashboard, name='dashboard'),

    url(r'^document/$', DocumentListView.as_view(), name='document'),
    url(r'^document/(?P<id>\d+)$', get_document_detail, name='document-detail'),

    url(r'^authors/$', AuthorsListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),

    url(r'^reserved/$', reservation_list, name='reservation-list'),
    url(r'^reserve_document/(?P<copy_id>[0-9a-z-]+)$', reserve_document, name='reserve-document'),

    url(r'^issued/$', giveout_list, name='giveout-list'),
    url(r'^issued/(?P<id>\d+)$', giveout_confirmation, name='giveout-confirmation'),

    url(r'^return_document/(?P<id>\d+)$', return_document, name='return-document'),

    url(r'^patrons/$', patrons_list, name='patrons-list'),
    url(r'^patrons/(?P<id>\d+)$', patron_details, name='patron-details'),
    url(r'^patrons/(?P<pk>\d+)/edit$', edit_patron, name='patron_edit'),
    url(r'^patrons/add$', add_patron, name='patron-add'),
    url(r'^patrons/(?P<pk>\d+)/delete$', delete_patron, name='patron-delete'),

    url(r'^document/create', DocumentCreate.as_view(), name='document-create'),
    url(r'^document/instance/create/(?P<pk>[0-9a-f-]+)$', instance_create, name='documentinstance-create'),
    url(r'^document/instance/update/(?P<id>[0-9a-f-]+)$', instance_update, name='documentinstance-update'),
    url(r'^document/instance/delete/(?P<id>[0-9a-f-]+)$', instance_delete, name='documentinstance-delete'),
    url(r'^document/instance/delete/confirm/(?P<id>[0-9a-f-]+)$', instance_deleteconfirm,
        name='documentinstance-deleteconfirm'),
    url(r'^document/update/(?P<pk>\d+)$', DocumentUpdate.as_view(), name='document-update'),
    url(r'^document/delete/(?P<pk>\d+)$', DocumentDelete.as_view(), name='document-delete'),

    url(r'^authors/create', author_create, name='author-create'),
    url(r'^authors/update/(?P<id>\d+)$', author_update, name='author-update'),
    url(r'^authors/delete/confirm/(?P<id>\d+)$', author_deleteconfirm, name='author-deleteconfirm'),
    url(r'^authors/delete/(?P<id>\d+)$', author_delete, name='author-delete'),

    url(r'^populate_database/$', populate_db, name='debug-populate-database'),
]

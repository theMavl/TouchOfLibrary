from django.conf.urls import url

from library.views.tag.tag_create import tag_create
from library.views.tag.tag_update import tag_update
from library.views.tag.tag_delete import tag_delete
from library.views.tag.tag_delete import tag_deleteconfirm

from library.views import *

# Maintenance routines
from library.models import Reservation
from library.views.author import author_create, author_delete
from library.views.author.author_delete import author_deleteconfirm
from library.views.author.author_update import author_update
from library.views.type.type_create import type_create
from library.views.type.type_update import type_update
from library.views.type.type_delete import type_delete
from library.views.type.type_delete import type_deleteconfirm
from library.views.document.priority_queue import get_priority_queue

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
    url(r'^notification_response/(?P<id>[0-9a-z-]+)$',
        notification_response, name='notification-response'),

    url(r'^request_document/(?P<document_id>\d+)$', request_document, name='request-document'),
    url(r'^edit_document_request/(?P<id>\d+)/(?P<action>[\w-]+)/$', edit_document_request,
        name='edit-document-request'),

    url(r'^issued/$', giveout_list, name='giveout-list'),
    url(r'^issued/(?P<id>\d+)$', giveout_confirmation, name='giveout-confirmation'),

    url(r'^return_document/(?P<id>\d+)$', return_document, name='return-document'),
    url(r'^renew_document/(?P<id>\d+)$', renew_document, name='renew-document'),

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
    url(r'^document/upload_photo', upload, name='document-upload-photo'),
    url(r'^document/upload_photo_complete', direct_upload_complete, name='document-upload-photo-complete'),
    url(r'^authors/create', author_create, name='author-create'),
    url(r'^authors/update/(?P<id>\d+)$', author_update, name='author-update'),
    url(r'^authors/delete/confirm/(?P<id>\d+)$', author_deleteconfirm, name='author-deleteconfirm'),
    url(r'^authors/delete/(?P<id>\d+)$', author_delete, name='author-delete'),

    url(r'^types/$', TypeListView.as_view(), name='types'),
    url(r'^types/(?P<pk>\d+)$', TypeDetailView.as_view(), name='types-detail'),
    url(r'^types/create', type_create, name='type-create'),
    url(r'^types/update/(?P<id>\d+)$', type_update, name='type-update'),
    url(r'^types/delete/confirm/(?P<id>\d+)$', type_deleteconfirm, name='type-deleteconfirm'),
    url(r'^types/delete/(?P<id>\d+)$', type_delete, name='type-delete'),

    url(r'^signup/$', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    url(r'^tags/$', TagListView.as_view(), name='tags'),
    url(r'^tags/create', tag_create, name='tag-create'),
    url(r'^tags/update/(?P<id>\d+)$', tag_update, name='tag-update'),
    url(r'^tags/delete/confirm/(?P<id>\d+)$', tag_deleteconfirm, name='tag-deleteconfirm'),
    url(r'^tags/delete/(?P<id>\d+)$', tag_delete, name='tag-delete'),

    url(r'^populate_database/$', populate_db, name='debug-populate-database'),
    url(r'^document/(?P<id>\d+)/queue$', get_priority_queue, name='priority_queue'),
]

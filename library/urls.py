from django.conf.urls import url

from . import views

# Maintenance routines
from library.models import Reservation

try:
    Reservation.clean_old_reservations()
except:
    pass

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^document/$', views.DocumentListView.as_view(), name='document'),
    url(r'^document/(?P<id>\d+)$', views.get_document_detail, name='document-detail'),

    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),

    url(r'^reserved/$', views.reservation_list, name='reservation-list'),
    url(r'^reserve_document/(?P<copy_id>[0-9a-z-]+)$', views.reserve_document, name='reserve-document'),

    url(r'^issued/$', views.giveout_list, name='giveout-list'),
    url(r'^issued/(?P<id>\d+)$', views.giveout_confirmation, name='giveout-confirmation'),

    url(r'^patrons/$', views.patrons_list, name='patrons-list'),
    url(r'^patrons/(?P<id>\d+)$', views.patron_details, name='patron-details'),

    url(r'^document/create', views.DocumentCreate.as_view(), name='document-create'),
    url(r'^document/instance/create', views.DocumentInstanceCreate.as_view(), name='documentinstance-create'),
    url(r'^document/instance/update/(?P<id>[0-9a-f-]+)$', views.my_view, name='documentinstance-update'),
    url(r'^document/update/(?P<pk>\d+)$', views.DocumentUpdate.as_view(), name='document-update'),
    url(r'^document/delete/(?P<pk>\d+)$', views.DocumentDelete.as_view(), name='document-delete'),

    url(r'^populate_database/$', views.populate_db, name='debug-populate-database'),
]

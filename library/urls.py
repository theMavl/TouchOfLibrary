from django.conf.urls import url

from . import views

# Maintenance routines
from library.models import WishList
WishList.clean_old_wishes()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^document/$', views.DocumentListView.as_view(), name='document'),
    url(r'^document/(?P<id>\d+)$', views.get_document_detail, name='document-detail'),
    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^orders/$', views.order_list, name='order-list'),
    url(r'^orders/(?P<id>\d+)$', views.order_confirmation, name='order-confirmation'),
    url(r'^order_document/(?P<copy_id>[0-9a-z-]+)$', views.order_document, name='order-document'),
    url(r'^records/$', views.record_list, name='record-list'),

]

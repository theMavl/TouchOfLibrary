from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
    url(r'^document/$', views.DocumentListView.as_view(), name='document'),
    url(r'^document/(?P<id>\d+)$', views.get_document_detail, name='document-detail'),
    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^book/(?P<id>[-\w]+)/order/$', views.order_book, name='order_book'),

]
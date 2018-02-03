from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='user_profile'),
    url(r'^document/$', views.DocumentListView.as_view(), name='document'),
    url(r'^document/(?P<id>\d+)$', views.get_document_detail, name='document-detail'),
    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^book/(?P<id>[-\w]+)/order/$', views.order_book, name='order_book'),

]

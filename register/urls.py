from django.conf.urls import url

from . import views


urlpatterns = [
      url(r'^$', views.index, name='index'),
      url(r'^document/$', views.DocumentListView.as_view(), name='document'),
      #url(r'^document/(?P<pk>\d+)$', views.DocumentDetailView.as_view(), name='document-detail'),
]

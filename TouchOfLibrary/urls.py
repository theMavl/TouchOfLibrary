"""TouchOfLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import TouchOfLibrary.views as views

urlpatterns = [
    path('admin/', admin.site.urls)
]

from django.conf.urls import include
from django.conf.urls import url

urlpatterns += [
    url(r'^library/', include('library.urls')),
    path('library/', include('library.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

from django.views.generic import RedirectView

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/library/', permanent=True)),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

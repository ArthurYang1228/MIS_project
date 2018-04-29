"""misproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from dialog import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^dialog/(?P<pk>\d+)/$', views.post),
    url(r'^register/$', views.register),
    url(r'^key/$', views.key_word),
    url(r'^key/new/$', views.new_key_word),
    url(r'^key/update/(?P<id>\d+)/$', views.update_key_word),
    url(r'^key/delete/(?P<id>\d+)/$', views.delete_key_word),
    url(r'^location/$', views.location),
    url(
        r'^chatterbot/',
        include('chatterbot.ext.django_chatterbot.urls',
        namespace='chatterbot')
    ),
]

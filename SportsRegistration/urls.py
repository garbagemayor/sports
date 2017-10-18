"""SportsRegistration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from . import view
from django.conf.urls.static import static
from django.conf import settings
from Events import views as  Events_view
from Users import views as  Users_view


urlpatterns = [
                  url(r'^$', view.HomePageView),
                  url(r'^events/$', Events_view.index),
                  url(r'^users/$', view.UsersView),
                  url(r'^authorized/$', Users_view.auth),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

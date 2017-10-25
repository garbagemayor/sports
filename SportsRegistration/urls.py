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
from django.views.generic import RedirectView
from django.conf import settings
from Events import views as  Events_view
from Users import views as  Users_view


urlpatterns = [
                  url(r'^$', view.HomePageView, name='homepage'),
                  url(r'^events/$', Events_view.index, name='eventslist'),
                  url(r'^events/(\d+)/$', Events_view.page, name='eventspage'),
                  url(r'^users/$', view.UsersView, name='user'),
                  url(r'^authorized/$', Users_view.auth, name='login'),
                  url(r'^logout/$', Users_view.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

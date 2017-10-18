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
<<<<<<< HEAD
from Events import views as  Events_view


urlpatterns = [
                  url(r'^$', view.HomePageView),
                  url(r'^events/$', Events_view.index),
                  url(r'^users/$', view.UsersView),
=======
from Events import view as events_view
from HomePage import view as homepage_view
from Users import view as users_view


urlpatterns = [
    url(r'^$', view.firstView),
    url(r'^events/$', events_view.index, name='events'),
    url(r'^login/$', users_view.login, name='login'),
    url(r'^user/$', users_view.profile, name='profile'),
>>>>>>> ccabf273b7190cc73584262f30b6394e7f85573c
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

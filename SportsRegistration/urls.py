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
from django.contrib import admin
from RegistrationRecord import views as Record_view


urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  
                  url(r'^$',  RedirectView.as_view(url='/main/')),
                  url(r'^main/$', view.HomePageView, name='homepage'),
                  url(r'^events/$', Events_view.index, name='eventslist'),
                  url(r'^events/(\d+)/$', Events_view.page, name='eventspage'),                  
                  url(r'^events/delete/(\d+)/$', Events_view.delete_events, name='deletepage'),                                    
                  url(r'^events/next/(\d+)/$', Events_view.nextphase, name='nextphase'),                                     
                  url(r'^events/sign/(\d+)/$', Events_view.sign, name='signpage'),                                     
                  url(r'^events/design/(\d+)/$', Events_view.design, name='designpage'), 
                  url(r'^user/$', Users_view.my_information, name='user'),
                  url(r'^authorized/$', Users_view.auth, name='login'),
                  url(r'^logout/$', Users_view.logout, name='logout'),
                  url(r'^edit_email/(\d+)$', Record_view.edit_email, name='edit_email'),
                  url(r'^user/myevents/$', Users_view.my_events, name='my_events'),
                  url(r'^managers/$', Users_view.manager, name='manager'),
                  url(r'^managers/(\d+)/$', Users_view.demanager, name='demanager'),
                  url(r'^events/addevents$', Events_view.addevents, name='addevents'), 
                  url(r'^record/(\d+)/$', Record_view.recordPage, name='recordpage'),
                  url(r'^qrcode/(\d+)/$', Events_view.qrcode, name='qrcode'),
                  url(r'^record_download_csv/(\d+)/$', Record_view.recordDownloadCSV, name='recorddownload'),
                  url(r'^record_download_xlsx/(\d+)/$', Record_view.recordDownloadXLSX, name='recorddownload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

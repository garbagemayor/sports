# -*- coding: utf-8 -*-

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
from HomePage import views as  HomePage_view
from Events import views as  Events_view
from Users import views as  Users_view
from django.contrib import admin
from RegistrationRecord import views as Record_view


urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  #主页
                  url(r'^$',  RedirectView.as_view(url='/main/')),
                  url(r'^main/$', HomePage_view.index, name='homepage'),

                  #赛事
                  url(r'^events/$', Events_view.index, name='eventslist'),                          #所有赛事页
                  url(r'^events/(\d+)/$', Events_view.page, name='eventspage'),                     #赛事详情页            
                  url(r'^events/delete/(\d+)/$', Events_view.delete_events, name='deletepage'),     #删除赛事                                  
                  url(r'^events/next/(\d+)/$', Events_view.nextphase, name='nextphase'),            #改变阶段                              
                  url(r'^events/sign/(\d+)/$', Events_view.sign, name='signpage'),                  #报名                      
                  url(r'^events/design/(\d+)/$', Events_view.design, name='designpage'),            #取消报名
                  url(r'^events/addevents$', Events_view.addevents, name='addevents'),              #添加赛事
                  url(r'^events/setprizes$', Events_view.addevents, name='setprize'),                  
                  url(r'^events/viewprizes$', Events_view.addevents, name='prize'), 
                  url(r'^qrcode/(\d+)/$', Events_view.qrcode, name='qrcode'),

                  #用户
                  url(r'^user/mypage/$', Users_view.my_information, name='user'),            #个人页
                  url(r'^user/alter/$', Users_view.alter, name='user'),                     #修改信息
                  url(r'^user/(\d+)/$', Users_view.others, name='others'),                  #浏览其他用户信息  （暂无）
                  url(r'^authorized/$', Users_view.auth, name='login'),                     #登录完成
                  url(r'^logout/$', Users_view.logout, name='logout'),                      #登出
                  url(r'^edit_email/(\d+)$', Record_view.edit_email, name='edit_email'),    #修改邮件
                  url(r'^user/myevents/$', Users_view.my_events, name='my_events'),         #查看我的赛事

                  #管理员
                  url(r'^managers/$', Users_view.manager, name='manager'),
                  url(r'^managers/(\d+)/$', Users_view.demanager, name='demanager'),        #删除管理员

                  #记录
                  url(r'^record/(\d+)/$', Record_view.recordPage, name='recordpage'),       #某赛事报名情况
                  url(r'^record_download_csv/(\d+)/$', Record_view.recordDownloadCSV, name='recorddownload'),
                  url(r'^record_download_xlsx/(\d+)/$', Record_view.recordDownloadXLSX, name='recorddownload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

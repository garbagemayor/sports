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
from django.conf.urls import url, include
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
    
                  # 主页
                  url(r'^$',  RedirectView.as_view(url='/main/')),
                  url(r'^main/$', HomePage_view.index, name='homepage'),

                  #赛事
                  url(r'^events/$', Events_view.index, name='eventslist'),                          #所有赛事页
                  url(r'^events/(\d+)/$', Events_view.page, name='eventspage'),                     #赛事详情页
                  # url(r'^events/(\d+)/maketeam/$',
                  #     Events_view.page_maketeam, name='eventspage_m'),                              #赛事详情页，并显示团队报名模块
                  # url(r'^events/(\d+)/maketeam/fn=([^;]*);sn=([^;]*);se=((\d+,)*)/$',
                  #     Events_view.page_maketeam_search_selected, name='eventspage_mss'),            #赛事详情页，并显示团队报名模块，带有搜索内容，以及已选队友
                  url(r'^events/static_refresh/fn=([^;]*);sn=([^;]*)/$',
                      Events_view.page_static_refresh_search, name='eventspage_ms'),                     #赛事详情页，带有搜索内容，只返回刷新部分html内容
                  url(r'^events/static_refresh/uid=(\d+)/$',
                      Events_view.page_static_refresh_selected, name='eventspage_ms'),                   #赛事详情页，带有选择对象，只返回刷新部分html内容
                  url(r'^events/delete/(\d+)/$', Events_view.delete_events, name='deletepage'),     #删除赛事                                  
                  url(r'^events/next/(\d+)/$', Events_view.nextphase, name='nextphase'),            #改变阶段                              
                  url(r'^events/sign/(\d+)/$', Events_view.sign, name='signpage'),                  #报名
                  url(r'^events/teamsign/(\d+)/se=((\d+,)*)/$',
                      Events_view.teamsign, name='teamsignpage'),                                   #团队报名
                  url(r'^events/design/(\d+)/$', Events_view.design, name='designpage'),            #取消报名
                  url(r'^events/addevents/$', Events_view.addevents, name='addevents'),              #添加赛事
                  url(r'^events/setprizes/(\d+)/$', Events_view.setprizes, name='setprize'),                  
                  url(r'^events/viewprizes/(\d+)/$', Events_view.viewprizes, name='prize'), 
                  url(r'^events/qrcode/$', Events_view.qrcode, name='qrcode'),

                  #用户
                  url(r'^user/$', Users_view.my_information, name='user'),           #个人页
                  url(r'^user/profile/$', Users_view.edit_information, name='user'),        #修改信息
                  url(r'^user/(\d+)/$', Users_view.others, name='others'),                  #浏览其他用户信息
                  url(r'^authorized/$', Users_view.auth, name='login'),                     #登录完成
                  url(r'^logout/$', Users_view.logout, name='logout'),                      #登出
                  url(r'^user/myevents/$', Users_view.my_events, name='my_events'),
                  url(r'^notification/$', Users_view.notification, name='notification'),
                  url(r'^notes/(\d+)$', Users_view.notes, name='notes'),
                  url(r'^mark_as_read/$', Users_view.mark_as_read, name='mark_as_read'),
                  url(r'^notification_count/$', Users_view.notification_count,
                      name='notification_count'),

                  # 管理员
                  url(r'^managers/$', Users_view.backend, name='backend'),
                  url(r'^managers/managers/$', Users_view.manager, name='manager'),
                  url(r'^managers/(\d+)/$', Users_view.demanager, name='demanager'),        # 删除管理员
                  url(r'^managers/team/$', Users_view.team, name='team'),
                  url(r'^managers/celebrity/$', Users_view.celebrity, name='celebrity'),
                  url(r'^managers/photos/$', Users_view.photos, name='photos'), 

                  # 记录
                  url(r'^record/(\d+)/$', Record_view.recordPage, name='recordpage'),       # 某赛事报名情况
                  url(r'^record_download_csv/(\d+)/$', Record_view.recordDownloadCSV, name='recorddownload'),
                  url(r'^record_download_xlsx/(\d+)/$', Record_view.recordDownloadXLSX, name='recorddownload'),
                  url(r'^record/confirm/$', Record_view.confirm, name='confirm'),       # 审核内容回复
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

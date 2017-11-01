# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events, Sign

# Create your views here.

def index(request):
    events1=list(Events.objects.filter(status=0)[-1:-7:-1])
    for l in events1:
        l.s2 = gets2(l.status)
        l.s3 = gets3(l.status)
    paginator=Paginator(events_list, 10)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    
    return render(request, 'Events/events.html', {'events_list':events_list})

def gets2(i):
    if i == 1:
        return "即将开始"
    elif i == 2:
        return "正在报名"
    elif i == 3:
        return "报名已截止"
    elif i == 4:
        return "比赛已结束"
    else:
        return "???"

def gets3(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"

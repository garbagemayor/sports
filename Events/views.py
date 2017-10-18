# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    events_list=list(Events.objects.all()[::-1])
    for l in events_list:
        if l.status =="success":
            l.s2 = "正在报名"
            l.s3 = "立即报名"
        elif l.status =="error":
            l.s2 = "已截止"
        elif l.status =="info":
            l.s2 = "尚未开始"
    paginator=Paginator(events_list, 3)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    
    return render(request, 'Events/events.html', {'events_list':events_list})
    
def page(request, Id):
    events=Events.objects.get(id=Id)
    return render(request, 'Events/page.html', {'events':events})

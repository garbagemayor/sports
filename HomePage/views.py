# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events, IMG, Users
from HomePage.models import Broadcast
from HomePage.models import utcToLocal
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    team = list(IMG.objects.filter(headline=True,imgtype=0))
    game = list(IMG.objects.filter(headline=True,imgtype=1))
    celebrity = list(IMG.objects.filter(headline=True,imgtype=2)) 
    broadcast_list = list(Broadcast.objects.all()[::-1])
    events_list=Events.objects.all()[::-1]
    events1=[]
    events2=[]
    events3=[]
    
    for e in events_list:
        if e.getStatus()==1:
            events1.append(e)
        if e.getStatus()==2:
            events2.append(e)
        if e.getStatus()==5:
            events3.append(e)
    if len(events1)>5:
        events1=events1[:5]
    if len(events2)>5:
        events2=events2[:5]
    if len(events3)>5:
        events3=events3[:5]
    if len(broadcast_list)>5:
        broadcast_list=broadcast_list[:5]

    return render(request, "HomePage/newhomepage.html",
                  {'events1': events1,
                   'events1_len' : len(events1),
                   'events2': events2,
                   'events2_len' : len(events2),
                   'events3': events3,
                   'events3_len' : len(events3),
                   'team': team,
                   'celebrity': celebrity,
                   'game': game,
                   'broadcast':broadcast_list})


def broadcast(request):
    broadcast_list = list(Broadcast.objects.all()[::-1])
    paginator = Paginator(broadcast_list, 10)
    page = request.GET.get('page')
    try:
        broadcast_list = paginator.page(page)
    except PageNotAnInteger:
        broadcast_list = paginator.page(1)
    except EmptyPage:
        broadcast_list = paginator.page(paginator.num_pages)

    return render(request, 'HomePage/broadcast.html', {'broadcast': broadcast_list})

def broadcastpage(request, Id):
    b = Broadcast.objects.filter(id=Id)
    if b:
        b=b[0]
        b.time = utcToLocal(b.time).strftime("%Y-%m-%d %H:%M:%S")
        b.publishername = Users.objects.get(id=b.publisher).name
        return render(request, 'HomePage/broadcastpage.html', {'broadcast': b})
    else:
        return render(request, 'HomePage/broadcastpage.html')


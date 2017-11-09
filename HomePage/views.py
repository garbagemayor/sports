# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events, IMG

# Create your views here.

def index(request):
    team = IMG.objects.filter(id=1)
    team = team[0]
    celebrity = list(IMG.objects.filter(imgtype=1))
    celebrity = celebrity[-1]
    photos = IMG.objects.filter(imgtype=2)
    print team.name
    print team.img.url
    print team.detail
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


    
    return render(request, "HomePage/newhomepage.html", {'events1':events1, 'events2':events2, 'events3':events3, 'team':team, 'celebrity':celebrity, 'photos':photos})


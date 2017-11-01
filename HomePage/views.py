# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events

# Create your views here.

def index(request):
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


    
    return render(request, "HomePage/newhomepage.html", {'events1':events1, 'events2':events2, 'events3':events3})


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events, Sign

# Create your views here.

def index(request):
    events1=list(Events.objects.filter(status=1)[::-1])
    events2=list(Events.objects.filter(status=2)[::-1])
    events3=list(Events.objects.filter(status=4)[::-1])
    if len(events1)>5:
        events1=events1[:5]
    if len(events2)>5:
        events2=events2[:5]
    if len(events3)>5:
        events3=events3[:5]


    
    return render(request, "HomePage/newhomepage.html", {'events1':events1, 'events2':events2, 'events3':events3})


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from HomePage.models import User 

# Create your views here.
def auth(request):
    r = requests.post('https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
            + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    print type(rr)
    print rr
    j = rr.json()
    print j.keys()
    User.objects.get_or_create(name=j['user']['name'])
    return render(request, "Users/authorized.html", rr.json()['user'])
    #  return HttpResponse(rr.json()['user'])

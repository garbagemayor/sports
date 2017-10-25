# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
import json
from HomePage.models import User 

# Create your views here.
def auth(request):
    r = requests.post('https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
            + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j=rr.json()
    user=User.objects.get_or_create(name=j['user']['name'], email=j['user']['email'], mobile=j['user']['mobile'], fullname=j['user']['fullname'], classnumber=j['user']['groups'][0])
    request.session['username']=j['user']['name']
    request.session['userid']=user[0].id;
    return HttpResponseRedirect("/events/")

def logout(request):
    if (request.session['username']):
        del request.session['username']
    return HttpResponseRedirect("/")

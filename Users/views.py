# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import json
from HomePage.models import User
from django.core.mail import send_mail

# Create your views here.
def auth(request):
    r = requests.post('https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
            + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j=rr.json()
    #User.objects.get_or_create(name=j['user']['name'], classNumber=j['user']['group'][0])
    request.session['username']=j['user']['name']
    return render(request, "Events/events.html")
    #  return HttpResponse(rr.json()['user'])

def logout(request):
    if (request.session['username']):
        del request.session['username']
    return render(request, "HomePage/homepage.html")

def send_email(request):
    email_title = 'title'
    email_body = 'content'
    EMAIL_FROM = '924486024@qq.com'
    email = 'luohy15@mails.tsinghua.edu.cn'
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    if send_status:
        return HttpResponseRedirect('/')

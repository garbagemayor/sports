# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import re
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from HomePage.models import Events
from HomePage.models import Signs as Sign
from HomePage.models import Users as User
from HomePage.models import IMG


def auth(request):
    r = requests.post(
        'https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
        + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j = rr.json()
    user = User.objects.get_or_create(name=j['user']['name'])
    if user[1]:
        User.objects.filter(name=j['user']['name']).update(email=j['user']['email'], mobile=j['user']['mobile'],
                                                           fullname=j['user']['fullname'],
                                                           classnumber=j['user']['groups'][0])
    request.session['username'] = j['user']['name']
    request.session['userid'] = user[0].id
    request.session['auth'] = user[0].authority
    messages.add_message(request, messages.INFO, '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
    return HttpResponseRedirect("/events/")


def logout(request):
    if request.session['username']:
        del request.session['username']
    if request.session['userid']:
        del request.session['userid']
    if request.session['auth']:
        del request.session['auth']
    messages.add_message(request, messages.INFO, '成功登出！')
    return HttpResponseRedirect("/")


def my_information(request):
    user_id = request.session['userid']
    info_list = {}
    if user_id:
        my_infos = User.objects.get(id=user_id)
        info_list['id'] = my_infos.name
        info_list['name'] = my_infos.fullname
        info_list['mobile'] = my_infos.mobile
        info_list['classnumber'] = my_infos.classnumber
        info_list['authority'] = my_infos.authority
        info_list['email'] = my_infos.email
        info_list['gender'] = my_infos.gender
        info_list['student_number'] = my_infos.student_number
        info_list['certification_type'] = my_infos.certification_type
        info_list['certification_id'] = my_infos.certification_id
        info_list['birthday'] = my_infos.birthday
        info_list['cloth_size'] = my_infos.cloth_size
        info_list['room_address'] = my_infos.room_address
        info_list['degree'] = my_infos.degree
    return render(request, "Users/my_information.html", info_list)


@csrf_exempt
def edit_information(request):
    user_id = request.session['userid']
    info_list = {}
    if user_id:
        my_infos = User.objects.get(id=user_id)
        info_list['id'] = my_infos.name
        info_list['name'] = my_infos.fullname
        info_list['classnumber'] = my_infos.classnumber
        info_list['authority'] = my_infos.authority
        info_list['gender'] = my_infos.gender
        info_list['mobile'] = my_infos.mobile
        info_list['email'] = my_infos.email
        info_list['student_number'] = my_infos.student_number
        info_list['certification_type'] = my_infos.certification_type
        info_list['certification_id'] = my_infos.certification_id
        info_list['birthday'] = my_infos.birthday
        info_list['cloth_size'] = my_infos.cloth_size
        info_list['room_address'] = my_infos.room_address
        info_list['degree'] = my_infos.degree
    if request.POST:
        if request.POST['gender'] == 'null':
            info_list['rlt'] = "请选择您的性别！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if request.POST['certification_type'] == 'null':
            info_list['rlt'] = "请选择您的证件类型！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if request.POST['degree'] == 'null':
            info_list['rlt'] = "请选择您的正在攻读的学位！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if request.POST['cloth_size'] == 'null':
            info_list['rlt'] = "请选择您的衣服尺码！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if legal_mobile(request.POST['mobile']) is None:
            info_list['rlt'] = "请输入正确的手机号码！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if legal_email(request.POST['email']) is None:
            info_list['rlt'] = "请输入正确的电子邮箱！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if legal_student_number(request.POST['student_number']) is None:
            info_list['rlt'] = "请输入正确的学号！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if not legal_certification_id(request.POST['certification_id']):
            info_list['rlt'] = "请输入正确的证件号！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)
        if legal_birthday(request.POST['birthday']) is None:
            info_list['rlt'] = "请输入正确的出生日期！"
            info_list.update(keep_info(request))
            return render(request, "Users/users.html", info_list)

        User.objects.filter(id=user_id).update(
            gender=request.POST['gender'],
            certification_type=request.POST['certification_type'],
            degree=request.POST['degree'],
            cloth_size=request.POST['cloth_size'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
            student_number=request.POST['student_number'],
            certification_id=request.POST['certification_id'],
            birthday=request.POST['birthday'],
            room_address=request.POST['room_address']
        )

        messages.add_message(request, messages.INFO, '修改成功！')
        return HttpResponseRedirect('/user/')
    # return render(request, "Users/users.html", info_list)
    return render_to_response("Users/users.html", info_list)


def my_events(request):
    if request.session['userid']:
        events_list = []
        elist = Sign.objects.filter(userId=request.session['userid'])
        for e in elist:
            tmp = Events.objects.filter(id=e.eventsid)
            if tmp:
                tmp = tmp[0]
                tmp.s2 = gets2(tmp.getStatus())
                events_list.append(tmp)
        paginator = Paginator(events_list, 3)
        page = request.GET.get('page')
        try:
            events_list = paginator.page(page)
        except PageNotAnInteger:
            events_list = paginator.page(1)
        except EmptyPage:
            events_list = paginator.page(paginator.num_pages)

        return render(request, 'Events/myevents.html', {'events_list': events_list})
    else:
        messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect("/authorized/")


def others(request, Id):
    user = User.objects.filter(id=Id)
    info_list = {}
    if user:
        my_infos = User.objects.get(id=Id)
        info_list['id'] = my_infos.name
        info_list['name'] = my_infos.fullname
        info_list['mobile'] = my_infos.mobile
        info_list['classnumber'] = my_infos.classnumber
        info_list['authority'] = my_infos.authority
        info_list['email'] = my_infos.email
        info_list['gender'] = my_infos.gender
        info_list['student_number'] = my_infos.student_number
        info_list['certification_type'] = my_infos.certification_type
        info_list['certification_id'] = my_infos.certification_id
        info_list['birthday'] = my_infos.birthday
        info_list['cloth_size'] = my_infos.cloth_size
        info_list['room_address'] = my_infos.room_address
        info_list['degree'] = my_infos.degree
        return render(request, 'Users/userpage.html', info_list)
    else:
        return HttpResponseRedirect('/main/')


@csrf_exempt
def manager(request):
    user = User.objects.filter().exclude(authority=0)
    for u in user:
        u.auth=getauth(u.authority)
    status = 0
    if request.method == "POST":
        if len(user) < 7:
            if len(User.objects.filter(name=request.POST['name'])) == 0:
                messages.add_message(request, messages.INFO, '查无此人！')
            else:
                user = User.objects.get(name=request.POST['name'])
                if user.authority < 1:
                    User.objects.filter(name=request.POST['name']).update(authority=1)
                    messages.add_message(request, messages.INFO, '成功将' + request.session['username'] + '升至管理员！')
                else:
                    messages.add_message(request, messages.INFO, '无此操作权限！')
            user = User.objects.filter(authority=1)
        else:
            messages.add_message(request, messages.INFO, '管理员数量已达上限！')
    return render(request, 'Users/manager.html', {'users_list': user, 'status': json.dumps(status)})


def demanager(request, Id):
    if request.session['auth'] > 1:
        u = User.objects.filter(id=Id)
        if u[0].authority > 1:
            messages.add_message(request, messages.INFO, u[0].fullname + '是超级管理员！')
        else:
            User.objects.filter(id=Id).update(authority=0)
            messages.add_message(request, messages.INFO, u[0].fullname + '已不再是管理员！')
    else:
        messages.add_message(request, messages.INFO, '无此操作权限！')
    return HttpResponseRedirect("/managers/")

def backend(request):
    return render(request, 'Users/backend.html')

@csrf_exempt
def team(request):
    if request.method == 'POST':
        new_img = IMG.objects.get(id=1)
        if len(request.POST['name'])>1:
            new_img.name=request.POST['name']
        if request.FILES.get('img'):
            new_img.img=request.FILES.get('img')
        if len(request.POST['name'])>1:
            new_img.detail=request.POST['detail']        
        new_img.save()
        return HttpResponseRedirect("/main/")
    return render(request, 'Users/team.html')

@csrf_exempt
def celebrity(request):
    if request.method == 'POST':
        new_img = IMG(
            name=request.POST['name'],
            img=request.FILES.get('img'),
            detail=request.POST['detail'],
            imgtype=1
        )
        new_img.save()
        return HttpResponseRedirect("/main/")
    return render(request, 'Users/celebrity.html')

@csrf_exempt
def photos(request):
    if request.method == 'POST':
        new_img = IMG(
            name=request.POST['name'],
            img=request.FILES.get('img'),
            detail=request.POST['detail'],
            imgtype=2
        )     
        new_img.save()
        return HttpResponseRedirect("/main/")
    return render(request, 'Users/team.html')

def gets2(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"


def getauth(i):
    if i == 0:
        return "普通用户"
    elif i == 1:
        return "管理员"
    elif i >= 2:
        return "超级管理员"


def keep_info(request):
    info_list = {'gender': request.POST['gender'], 'mobile': request.POST['mobile'], 'email': request.POST['email'],
                 'student_number': request.POST['student_number'],
                 'certification_type': request.POST['certification_type'],
                 'certification_id': request.POST['certification_id'], 'birthday': request.POST['birthday'],
                 'cloth_size': request.POST['cloth_size'], 'room_address': request.POST['room_address'],
                 'degree': request.POST['degree']}
    return info_list


def legal_mobile(mobile):
    pattern = "^1[0-9]{10}$"
    return re.match(pattern, mobile)


def legal_email(email):
    pattern = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
    return re.match(pattern, email)


def legal_student_number(student_number):
    pattern = "^20[0-9]{8}$"
    return re.match(pattern, student_number)


def legal_certification_id(certification_id):
    return certification_id != "尚未登记" and certification_id != ""


def legal_birthday(birthday):
    pattern = "^(199[0-9]|20[0-9]{2})-[0-9]{2}-[0-9]{2}$"
    return re.match(pattern, birthday)

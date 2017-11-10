# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import re
import requests
from Users.models import Notification
from Users.models import NotificationController
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from RegistrationRecord.forms import EmailForm

from HomePage.models import Events
from HomePage.models import Signs as Sign
from HomePage.models import Users as User
from HomePage.models import IMG

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import django.utils.timezone as timezone

"""
def auth(request):
    r = requests.post(
        'https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
        + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j = rr.json()
    user = User.objects.get_or_create(name=j['user']['name'])
    #  if user[1]:
    User.objects.filter(name=j['user']['name']).update(email=j['user']['email'], mobile=j['user']['mobile'],
                                                           fullname=j['user']['fullname'],
                                                           classnumber=j['user']['groups'][0])
    request.session['username'] = j['user']['name']
    request.session['userid'] = user[0].id
    print "user = ", user
    print "session.userid = ", request.session['userid']
    request.session['auth'] = user[0].authority
    messages.add_message(request, messages.INFO, '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
    return HttpResponseRedirect("/events/")
"""

def auth(request):
    r = requests.post(
        'https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
        + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j = rr.json()
    user = User.objects.filter(name=j['user']['name'])
    isNewUser = len(user) == 0
    if isNewUser:
        User.objects.create(name=j['user']['name'])
    user = User.objects.get(name=j['user']['name'])


    # 先获取一堆信息出来再说
    user_name = j['user']['name']
    user_fullname = j['user']['fullname']
    user_mobile = j['user']['mobile']
    user_email = j['user']['email']
    user_birthday = j['user']['birthdate']
    user_birthday = user_birthday[0:4] + '-' + user_birthday[4:6] + '-' + user_birthday[6:8]
    user_classnumber = None
    user_degree = None
    if j['user']['bachelor']['year'] != None:
        user_classnumber = u'计算机系' + unicode(str(j['user']['bachelor']['year'])) + u'级' + unicode(str(j['user']['bachelor']['classNumber'])) + u'班'
        user_degree = 0
    if j['user']['master']['year'] != None:
        user_classnumber = u'计算机系研究生' + j['user']['master']['year'] + u'级' + j['user']['master']['classNumber'] + u'班'
        user_degree = 1
    if j['user']['doctor']['year'] != None:
        user_classnumber = u'计算机系博士' + j['user']['doctor']['year'] + u'级' + j['user']['doctor']['classNumber'] + u'班'
        user_degree = 2

    if isNewUser:
        # 如果是新用户，把信息填写到数据库
        user.authority = 0
        user.name = user_name
        user.fullname = user_fullname
        user.mobile = user_mobile
        user.email = user_email
        user.birthday = user_birthday
        user.classnumber = user_classnumber
        user.degree = user_degree
        user.save()

    # 然后把信息弄到reqest里面去
    request.session['username'] = user.name
    request.session['userid'] = user.id
    request.session['auth'] = user.authority

    # 如果是老用户，检测信息是否一致
    isDifferent = False
    if not isNewUser:
        if user.name != user_name                       \
            or user.fullname != user_fullname           \
            or user.mobile != user_mobile               \
            or user.email != user_email                 \
            or user.birthday != user_birthday           \
            or user.classnumber != user_classnumber     \
            or user.degree != user_degree:
            isDifferent = True

    # 弹出各种情况下的消息窗口
    if isNewUser:
        messages.add_message(request, messages.INFO,
                             '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
        messages.add_message(request, messages.INFO,
                             '检测到您是首次登录这个系统，请立即补充个人信息否则封号！')
        return HttpResponseRedirect("/user/profile/")
    elif isDifferent:
        messages.add_message(request, messages.INFO,
                             '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
        messages.add_message(request, messages.INFO,
                             '检测到你的个人信息与account9上的信息存在差异，请立即修改否则封号！')
        return HttpResponseRedirect("/user/profile/")
    else:
        messages.add_message(request, messages.INFO,
                             '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
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
        print "my_information: user_id = ", user_id
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
            tmp = Events.objects.filter(id=e.eventId)
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
        return HttpResponseRedirect("https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host()+"/authorized")


def others(request, Id):
    user = User.objects.filter(id=Id)
    info_list = {}
    if user:
        my_infos = User.objects.get(id=Id)
        info_list['userid'] = Id
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

def send_message(request, user_id):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data['title']
            c = form.cleaned_data['content']
            Notification.objects.create(sender=request.session['userid'],
                    target=user_id, title=t, content=c, createTime=timezone.now())
            return HttpResponseRedirect('/user/' + str(user_id))
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})
    else:
        form = EmailForm()
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})

def notification(request):
    if request.method == 'POST':
        checkbox_list=request.POST.getlist("checked")
        for i in checkbox_list:
            Notification.objects.filter(id=i).delete()
        user_id = request.session['userid']
        record_list = list(Notification.objects.filter(target=user_id))
        # 分页模块
        paginator=Paginator(record_list, 10)
        page = request.GET.get('page')
        try:
            record_list = paginator.page(page)
        except PageNotAnInteger:
            record_list = paginator.page(1)
        except EmptyPage:
            record_list = paginator.page(paginator.num_pages)
        message_map = {}
        message_map['record_list'] = record_list
        return render(request, 'Users/notification.html', message_map)
    user_id = request.session['userid']
    record_list = list(Notification.objects.filter(target=user_id))
    # 分页模块
    paginator=Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        record_list = paginator.page(page)
    except PageNotAnInteger:
        record_list = paginator.page(1)
    except EmptyPage:
        record_list = paginator.page(paginator.num_pages)
    message_map = {}
    message_map['record_list'] = record_list
    return render(request, 'Users/notification.html', message_map)

def notification_count(request):
    user_id = request.session['userid']
    print "notification_count: user_id = ", user_id
    obj = NotificationController.objects.get_or_create(userId=user_id)
    return HttpResponse(obj[0].unReadCount)

def notes(request, note_id):
    message_map = {}
    message_map['note'] = Notification.objects.get(id=note_id)
    request.session['noteid'] = note_id
    return render(request, 'Users/note.html', message_map)

def mark_as_read(request):
    note_id = request.session['noteid']
    user_id = request.session['userid']
    if not Notification.objects.get(id=note_id).isRead:
        Notification.objects.filter(id=note_id).update(isRead=True)
        obj = NotificationController.objects.get(userId=user_id)
        obj.unReadCount = obj.unReadCount - 1
        obj.save()
        return HttpResponse(obj.unReadCount)
    count = NotificationController.objects.get(userId=user_id).unReadCount
    return HttpResponse(count)

@receiver(post_save, sender=Notification)
def incr_notifications_counter(sender, instance, created, **kwargs):
    obj = NotificationController.objects.get_or_create(userId=instance.target)
    if not obj[1]:
        obj[0].unReadCount = obj[0].unReadCount + 1
        obj[0].save()

@receiver(post_delete, sender=Notification)
def decr_notifications_counter(sender, instance, **kwargs):
    if not instance.isRead:
        obj = NotificationController.objects.get_or_create(userId=instance.target)
        if not obj[1]:
            obj[0].unReadCount = obj[0].unReadCount - 1
            obj[0].save()

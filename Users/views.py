# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

import django.utils.timezone as timezone
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth

from HomePage.models import Events
from HomePage.models import IMG, Team
from HomePage.models import Signs as Sign
from HomePage.models import Users as User
from HomePage.models import utcToLocal
from Users.forms import EditForm
from Users.models import Notification
from Users.models import NotificationController
from django.core import serializers

designer_name = ["steventang", "luoy15", "yangjy15"]

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
    if j['user']['bachelor']['year'] is not None:
        user_classnumber = u'计算机系' + unicode(str(j['user']['bachelor']['year'])) + u'级' + unicode(
            str(j['user']['bachelor']['classNumber'])) + u'班'
        user_degree = 0
    if j['user']['master']['year'] is not None:
        user_classnumber = u'计算机系研究生' + j['user']['master']['year'] + u'级' + j['user']['master']['classNumber'] + u'班'
        user_degree = 1
    if j['user']['doctor']['year'] is not None:
        user_classnumber = u'计算机系博士' + j['user']['doctor']['year'] + u'级' + j['user']['doctor']['classNumber'] + u'班'
        user_degree = 2

    if isNewUser:
        # 如果是新用户，把信息填写到数据库
        user.authority = 2 if user.name in designer_name else 0
        user.name = user_name
        user.fullname = user_fullname
        user.mobile = user_mobile
        user.email = user_email
        user.birthday = user_birthday
        user.classnumber = user_classnumber
        user.degree = user_degree
        user.save()

    # 然后把信息弄到request.session里面去
    request.session['username'] = user.name
    request.session['userid'] = user.id
    request.session['auth'] = user.authority

    # 如果是老用户，检测信息是否一致
    isDifferent = False
    if not isNewUser:
        user.login_cnt += 1
        # 如果这个老用户，居然还能从account9上获取到新信息，也就忍了
        if user.name is None:
            user.name = user_name
            user.save()
        if user.fullname is None:
            user.fullname = user_fullname
            user.save()
        if user.mobile is None:
            user.mobile = user_mobile
            user.save()
        if user.email is None:
            user.email = user_email
            user.save()
        if user.birthday is None:
            user.birthday = user_birthday
            user.save()
        if user.classnumber is None:
            user.classnumber = user_classnumber
            user.save()
        if user.degree is None:
            user.degree = user_degree
            user.save()
        # 检查老用户信息是否一致，如果不一致，封号哭哭哟
        if user.name != user_name \
                or user.fullname != user_fullname \
                or user.mobile != user_mobile \
                or user.email != user_email \
                or user.birthday != user_birthday \
                or user.classnumber != user_classnumber \
                or user.degree != user_degree:
            isDifferent = True

    # 检测其他一些，从account9上获取不到的信息
    needMore = False
    if user.certification_id is None \
            or user.student_number is None \
            or user.cloth_size is None \
            or user.gender is None:
        needMore = True

    # 弹出各种情况下的消息窗口
    messages.add_message(request, messages.INFO, '登陆成功! ' + request.session['username'] + ' 欢迎来到体育赛事报名平台！')
    if isNewUser:
        messages.add_message(request, messages.INFO, '检测到您是首次登录这个系统，请立即补充个人信息，否则无法报名比赛！')
    elif isDifferent:
        messages.add_message(request, messages.INFO, '检测到你的个人信息与account9上的信息存在差异，请立即检查以免与个人信息不符！')
    elif needMore:
        messages.add_message(request, messages.INFO, '检测到您还需要填写更多信息，请立即填写，否则无法报名比赛！')
    else:
        return HttpResponseRedirect("/events/")
    return HttpResponseRedirect("/user/profile/")


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
    user_id = request.session.get('userid')
    if not user_id:
        return HttpResponseRedirect("/")
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
        # 新用户反手就给用户发送一个站内信
        uf = User.objects.filter(id=user_id)
        if len(uf) == 1:
            if uf[0].login_cnt == 1:
                Notification.objects.create(
                    sender=u"系统",
                    target=user_id,
                    title=u"欢迎使用体育赛事报名平台！",
                    content=u"建议立即仔细阅读<a href=\"/faq/\">《体育赛事报名平台服务协议》</a>")

        return HttpResponseRedirect('/user/')
    return render(request, "Users/users.html", info_list)
    # return render_to_response("Users/users.html", info_list)


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
        events_list_len = len(events_list)
        print "events_list_len", events_list_len
        paginator = Paginator(events_list, 3)
        page = request.GET.get('page')
        try:
            events_list = paginator.page(page)
        except PageNotAnInteger:
            events_list = paginator.page(1)
        except EmptyPage:
            events_list = paginator.page(paginator.num_pages)

        return render(request, 'Events/myevents.html',
                      {'events_list': events_list,
                       'events_list_len': events_list_len})
    else:
        messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect(
            "https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://" + request.get_host() + "/authorized")


def others(request, Id):
    # POST的时候就发出
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data['title']
            c = form.cleaned_data['content']
            Notification.objects.create(sender=request.session['username'], senderId=request.session['userid'],
                                        target=Id, title=t, content=c, createTime=timezone.now())
    user = User.objects.filter(id=Id)
    if user:
        # 没有POST就搞一个新的form
        form = EditForm()
        info_list = {'form': form}
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
    status = 0
    if request.method == "POST":
        if request.session.get('auth') < 2:
            messages.add_message(request, messages.INFO, "无此操作权限！")
        elif len(user) >= 7:
            messages.add_message(request, messages.INFO, '管理员数量已达上限！')
        else:
            if len(User.objects.filter(name=request.POST['name'])) == 0:
                messages.add_message(request, messages.INFO, '查无此人！')
            else:
                user = User.objects.get(name=request.POST['name'])
                if user.authority < 1:
                    User.objects.filter(name=request.POST['name']).update(authority=1)
                    messages.add_message(request, messages.INFO, '成功将' + request.POST['name'] + '升至管理员！')
                else:
                    messages.add_message(request, messages.INFO, '已经是管理员了！')
            user = User.objects.filter().exclude(authority=0)
    for u in user:
        u.auth = getauth(u.authority)
    return render(request,
                  'Users/manager.html', {
                      'session_auth': request.session['auth'],
                      'session_name': request.session['username'],
                      'session_userid': request.session['userid'],
                      'users_list': user,
                      'status': json.dumps(status)
                  })


def demanager(request, Id):
    u = User.objects.filter(id=Id)
    if len(u) != 1:
        messages.add_message(request, messages.INFO, "出错了！")
        return HttpResponseRedirect("/")
    u = u[0]
    if request.session.get('auth') == 2:
        if u.authority == 2:
            cnt = len(User.objects.filter(authority=2))
            if cnt <= 1:
                messages.add_message(request, messages.INFO, "不能降级！降级之后平台就没有超级管理员了！")
            else:
                User.objects.filter(id=Id).update(authority=1)
                if request.session.get('userid') == int(Id):
                    request.session['auth'] = 1
                messages.add_message(request, messages.INFO, "成功将" + u.name + "降至管理员！")
        elif u.authority == 1:
            User.objects.filter(id=Id).update(authority=0)
            messages.add_message(request, messages.INFO, "成功将" + u.name + "降至用户！")
    elif request.session.get('auth') == 1:
        if u.id == request.session['userid']:
            User.objects.filter(id=Id).update(authority=0)
            request.session['auth'] = 0
            messages.add_message(request, messages.INFO, "成功将" + u.name + "降至用户！")
            return HttpResponseRedirect("/")
    else:
        messages.add_message(request, messages.INFO, '无此操作权限！')
    return HttpResponseRedirect("/managers/managers/")

def inmanager(request, Id):
    if request.session.get('auth') == 2:
        u = User.objects.filter(id=Id)
        if len(u) != 1:
            messages.add_message(request, messages.INFO, "出错了！")
            return HttpResponseRedirect("/")
        u = u[0]
        if u.authority == 1:
            User.objects.filter(id=Id).update(authority=2)
            messages.add_message(request, messages.INFO, "成功将" + u.name + "升至超级管理员！")
    else:
        messages.add_message(request, messages.INFO, '无此操作权限！')
    return HttpResponseRedirect("/managers/managers/")

def backend(request):
    return render(request, 'Users/backend.html')


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


"""
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
"""


def notification(request):
    if request.method == 'POST':
        checkbox_list = request.POST.getlist("checked")
        for i in checkbox_list:
            Notification.objects.filter(id=i).delete()
    user_id = request.session['userid']
    record_list = list(Notification.objects.filter(target=user_id))
    record_list = record_list[::-1]
    for record in record_list:
        record.createTimeStr = utcToLocal(record.createTime).strftime("%Y-%m-%d %H:%M:%S")
    record_list_len = len(record_list)
    # 分页模块
    paginator = Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        record_list = paginator.page(page)
    except PageNotAnInteger:
        record_list = paginator.page(1)
    except EmptyPage:
        record_list = paginator.page(paginator.num_pages)
    message_map = {
        'record_list': record_list,
        'record_list_len': record_list_len
    }
    return render(request, 'Users/notification.html', message_map)


def notification_count(request):
    user_id = request.session['userid']
    obj = NotificationController.objects.get_or_create(userId=user_id)
    return HttpResponse(obj[0].unReadCount)


def notes(request, note_id):
    obj = Notification.objects.get(id=note_id)
    message_map = {}
    message_map['note'] = obj
    message_map['note_s'] = serializers.serialize("json", [obj,])
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


def qiniu_uptoken(request):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'iuFSDhrkjCI_bYpSCzZumRBlYNZ48oVC6UZN9b4R'
    secret_key = 'IwYY8y0rNGhueVayu2k2e-o1m6jDQ4KOmHEkPmet'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'lroot'
    # 上传到七牛后保存的文件名
    # key = ''
    # 生成上传 Token，可以指定过期时间等
    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200'
    }
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name)
    token_dict = {'uptoken': token}
    return JsonResponse(token_dict)


def new_img(request):
    new_img = IMG(
        url=request.POST['url'],
        detail=request.POST['detail'],
        imgtype=request.POST['imgtype'],
    )
    new_img.save()
    return HttpResponse('new a img')


def set_img(request):
    checkbox_list = request.POST['idlist']
    option = int(request.POST['option'])
    for checked_item in re.findall(r'\d+', checkbox_list):
        if option == -2: # 首页背景
            IMG.objects.filter(imgtype=-2).update(imgtype=0,headline=False)
            IMG.objects.filter(id=int(checked_item)).update(imgtype=-2,imgtypename=Team.objects.get(id=option).name,headline=True)
        elif option == -1: # 风采展示
            IMG.objects.filter(id=int(checked_item)).update(imgtype=-1,imgtypename=Team.objects.get(id=option).name,headline=True)
        elif option == -3: # 撤回
            IMG.objects.filter(id=int(checked_item)).update(headline=False)
        elif option == -4: # 删除
            IMG.objects.filter(id=int(checked_item)).delete()
        else:
            IMG.objects.filter(id=int(checked_item)).update(imgtypename=Team.objects.get(id=option).name,imgtype=option)
    return HttpResponse('set img ok')

def team(request):
    mmap = {'team_list': [], 'celebrity_list': []}
    mmap['team_list'] = list(Team.objects.filter(cate=1))
    mmap['celebrity_list'] = list(Team.objects.filter(cate=2))
    return render(request, 'Users/team.html', mmap)

def picture(request):
    from Manager.forms import OptionForm
    mmap = {'img_list': []}
    mmap['background_list'] = list(IMG.objects.filter(imgtype=-2))
    mmap['game_list'] = list(IMG.objects.filter(imgtype=-1))
    mmap['option_form'] = OptionForm()
    for img in list(IMG.objects.all()):
        mmap['img_list'].append(img)
    return render(request, 'Users/picture.html', mmap)

def imglist(requests):
    id_list = requests.POST['id_list']
    cate = requests.POST['cate']
    urlmap = {}
    for i in re.findall(r'\d+', id_list):
        imglist = list(IMG.objects.filter(imgtype=int(i)))
        urlmap['team' + i] = []
        urlmap['celebrity' + i] = []
        for img in imglist:
            urlmap['team' + i].append(img.url)
            urlmap['celebrity' + i].append(img.url)
    return JsonResponse(urlmap)

def note_content(requests):
    noteid = int(requests.session['noteid'])
    obj = Notification.objects.get(id=noteid)
    if obj.welcome:
        content = '- 亲爱的' + requests.session['username'] + ":\n" + obj.content
    else:
        content = obj.content        
    return HttpResponse(content)

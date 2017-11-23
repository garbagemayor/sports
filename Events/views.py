# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Signs as Sign
from HomePage.models import Events, Users
from HomePage.models import utcToLocal
from HomePage.models import Broadcast
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
import django.utils.timezone as timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.contrib import messages
import pyqrcode, io


# Create your views here.

def index(request):
    events_list = list(Events.objects.all()[::-1])
    for l in events_list:
        l.s2 = gets2(l.getStatus())
        l.s3 = gets3(l.getStatus())
        l.s4 = gets4(l.getStatus())
        l.timeRegStStr = utcToLocal(l.timeRegSt).strftime("%Y-%m-%d %H:%M:%S")
        l.timeRegEnStr = utcToLocal(l.timeRegEn).strftime("%Y-%m-%d %H:%M:%S")
        l.timeEvnStStr = utcToLocal(l.timeEvnSt).strftime("%Y-%m-%d %H:%M:%S")
    events_list_len = len(events_list)
    paginator = Paginator(events_list, 10)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    return render(request, 'Events/events.html',
                  {'events_list': events_list,
                   'events_list_len': events_list_len})


@csrf_exempt
def page(request, Id):
    events = Events.objects.get(id=Id)
    events.status = events.getStatus()
    events.s2 = gets2(events.getStatus())
    events.s3 = gets3(events.getStatus())
    events.timeRegStStr = utcToLocal(events.timeRegSt).strftime("%Y-%m-%d %H:%M:%S")
    events.timeRegEnStr = utcToLocal(events.timeRegEn).strftime("%Y-%m-%d %H:%M:%S")
    events.timeEvnStStr = utcToLocal(events.timeEvnSt).strftime("%Y-%m-%d %H:%M:%S")
    request.session['eventsid'] = Id
    return render(request, 'Events/page.html', {'events': events, "request": request})


@csrf_exempt
def page_static_refresh_search(request, searchFullName='', searchStudentNumber=''):
    # 从数据库中找出搜索到的结果
    print "searchFullName = ", searchFullName
    print "searchStudentNumber = ", searchStudentNumber
    if searchFullName == "":
        if searchStudentNumber == "":
            searchUserList = []
        else:
            searchUserList = list(Users.objects.filter(student_number=searchStudentNumber))
    else:
        if searchStudentNumber == "":
            searchUserList = list(Users.objects.filter(fullname=searchFullName))
        else:
            searchUserList = list(Users.objects.filter(fullname=searchFullName, student_number=searchStudentNumber))
    print "searchUserList = ", searchUserList
    return render(request, 'Events/page_static_refresh.html',
                  {"searchUserList": searchUserList,
                   "refresh_mode": "search",
                   "request": request})


@csrf_exempt
def page_static_refresh_selected(request, searchUserId=''):
    # 从数据库中找出搜索到的结果
    print "searchUserId = ", searchUserId
    searchUserList = list(Users.objects.filter(id=int(searchUserId)))
    print "searchUserList = ", searchUserList
    return render(request, 'Events/page_static_refresh.html',
                  {"searchUserList": searchUserList,
                   "refresh_mode": "selected"})


def set_prizes_static_refresh(request, numberList='', others=''):
    print "number = ", numberList, "others = ", others
    text = 'succeeded'
    n_list = numberList.split(',')
    print "n_list = ", n_list
    for i in range(1, 9):
        u = Users.objects.filter(student_number=n_list[i])
        if len(u) == 0 and n_list[i] != '0':
            text = n_list[i]
    return HttpResponse(text)


@csrf_exempt
def page_maketeam_search_selected(request, eventId, searchFullName='', searchStudentNumber='', selectedStr='',
                                  other=""):
    event = Events.objects.get(id=eventId)
    event.status = event.getStatus()
    event.s2 = gets2(event.getStatus())
    event.s3 = gets3(event.getStatus())
    # 从数据库中找出搜索到的结果
    print "searchFullName = ", searchFullName
    print "searchStudentNumber = ", searchStudentNumber
    if searchFullName == "":
        if searchStudentNumber == "":
            searchUserList = []
        else:
            searchUserList = list(Users.objects.filter(student_number=searchStudentNumber))
    else:
        if searchStudentNumber == "":
            searchUserList = list(Users.objects.filter(fullname=searchFullName))
        else:
            searchUserList = list(Users.objects.filter(fullname=searchFullName, student_number=searchStudentNumber))
    print "searchUserList = ", searchUserList
    # 从数据库中找出选中的结果
    print "selectedStr = ", selectedStr, type(selectedStr)
    selectedUserList = []
    selectedUserIdSet = set()
    if len(selectedStr) > 0:
        for userId in selectedStr.split(","):
            print "userId = ", userId, type(userId)
            if len(userId) > 0:
                userIdInt = int(userId)
                if userIdInt not in selectedUserIdSet:
                    selectedUserIdSet.add(userIdInt)
                    selectedUserList.append(Users.objects.filter(id=userIdInt)[0])
    print "selectedUserList = ", selectedUserList

    return render(request, 'Events/page.html',
                  {'events': event,
                   "maketeam": True,
                   "fullName": searchFullName,
                   "studentNumber": searchStudentNumber,
                   "selectedStr": selectedStr,
                   "searchUserList": searchUserList,
                   "selectedUserList": selectedUserList,
                   })


def delete_events(request, Id):
    events = Events.objects.get(id=Id)
    if request.method == "GET":
        if request.session.get('userid'):
            if request.session['auth'] > 0:
                Events.objects.filter(id=Id).delete()
                Sign.objects.filter(eventId=Id).delete()
                messages.add_message(request, messages.INFO, '删除成功！')
            else:
                messages.add_message(request, messages.INFO, '当前用户无此操作权限！')
        else:
            # messages.add_message(request, messages.INFO, '请登录！')
            return HttpResponseRedirect(
                'https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host+"/authorized')

        return HttpResponseRedirect('/events/')
    else:
        return HttpResponseRedirect('/events/')


def setprizes(request, Id):
    events = Events.objects.get(id=Id)
    Sign.objects.filter(eventId=Id).delete()
    if request.method == "POST":
        for i in range(1, 9):
            u = Users.objects.filter(student_number=request.POST['number_' + str(i)])
            if len(u) == 0:
                continue
            u = u[0]
            s = Sign.objects.filter(userId=u.id, eventId=Id)
            if len(s) == 0:
                Sign.objects.create(userId=u.id, eventId=Id)
            Sign.objects.filter(userId=u.id, eventId=Id).update(score=request.POST['score_' + str(i)], prize=i)
        return HttpResponseRedirect('/events/viewprizes/' + Id + '/')

    return render(request, 'Events/setprizes.html', {'event': events, 'prize_number': range(1, 9)})


def viewprizes(request, Id):
    events = Events.objects.get(id=Id)
    s = Sign.objects.filter(eventId=Id).exclude(prize='0')
    prize_list = []
    print "prize length : ", len(s)
    for i in s:
        prize = {'rank': i.prize}
        user = Users.objects.get(id=i.userId)
        prize['number'] = user.student_number
        prize['name'] = user.fullname
        prize['score'] = i.score
        prize_list.append(prize)
    return render(request, 'Events/prizes.html', {'event': events, 'prize_list': prize_list, 'prize_list_len' : len(prize_list)})


def nextphase(request, Id):
    events = Events.objects.get(id=Id)
    if request.method == "GET":
        if request.session['userid']:
            if request.session['auth'] > 0:
                e = Events.objects.get(id=Id)
                e.status += 1
                if e.status >= 5:
                    e.status = 1
                e.save()
                messages.add_message(request, messages.INFO, '修改成功！')
            else:
                messages.add_message(request, messages.INFO, '当前用户无此操作权限！')
        else:
            # messages.add_message(request, messages.INFO, '请登录！')
            return HttpResponseRedirect(
                'https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host+"/authorized')
        return HttpResponseRedirect('/events/' + Id)
    else:
        return HttpResponseRedirect('/events/' + Id)


def sign(request, Id):
    events = Events.objects.get(id=Id)
    if request.session.get('userid'):
        sf = Sign.objects.filter(userId=request.session['userid'], eventId=Id)
        if len(sf) >= 1:
            messages.add_message(request, messages.INFO, '请勿重复报名！')
        else:
            e = Events.objects.get(id=Id)
            if e.maxRegCnt != -1 and e.maxRegCnt <= e.nowRegCnt:
                messages.add_message(request, messages.INFO, '报名已经满了，你是怎么点到报名按钮的？')
            else:
                e.nowRegCnt += 1;
                e.save()
                Sign.objects.create(userId=request.session['userid'], eventId=Id)
                s = Sign.objects.get(userId=request.session['userid'], eventId=Id)
                s.teamSize = 1
                s.timeReg = timezone.now()
                s.exmStatus = 1
                s.save()
                messages.add_message(request, messages.INFO, '报名成功！')
    else:
        # messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect(
            'https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host+"/authorized')

    return HttpResponseRedirect('/events/' + Id + '/');


def teamsign(request, eventId, selectedStr="", other=""):
    event = Events.objects.get(id=eventId)
    if request.session.get('userid'):
        sf = Sign.objects.filter(userId=request.session['userid'], eventId=eventId)
        if len(sf) >= 1:
            messages.add_message(request, messages.INFO, '请勿重复报名！')
        else:
            # 获取团队成员的userId，去重
            teammateId = []
            for userId in selectedStr.split(","):
                if len(userId) > 0 and int(userId) not in teammateId:
                    teammateId.append(int(userId))
            if request.session['userid'] not in teammateId:
                teammateId.append(request.session['userid'])
            e = Events.objects.get(id=eventId)
            if e.maxRegCnt != -1 and e.maxRegCnt <= e.nowRegCnt:
                messages.add_message(request, messages.INFO, '报名已满！')
            else:
                e.nowRegCnt += 1;
                e.save()
                # 向数据库中添加
                Sign.objects.create(userId=request.session['userid'], eventId=eventId)
                s = Sign.objects.get(userId=request.session['userid'], eventId=eventId)
                s.teamSize = len(teammateId)
                s.teamMate = teammateId
                s.timeReg = timezone.now()
                s.exmStatus = 1
                s.save()
                #  messages.add_message(request, messages.INFO, '向数据库添加团队报名信息成功！')
    else:
        # messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect(
            'https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host+"/authorized')
    return HttpResponseRedirect('/events/' + eventId + '/');


def design(request, Id):
    events = Events.objects.get(id=Id)
    if request.session['userid']:
        sf = Sign.objects.filter(userId=request.session['userid'], eventId=Id)
        if len(sf) == 0:
            messages.add_message(request, messages.INFO, '您尚未报名！')
        else:
            if len(sf) >= 2:
                messages.add_message(request, messages.INFO, '您怎么这么强啊，居然在这一个比赛里面报次%d个名！您这么强，您爸妈知道吗？' % (len(sf)))
            e = Events.objects.get(id=Id)
            for s in sf:
                if s.exmStatus == 1 or s.exmStatus == 3:
                    if e.nowRegCnt > 0:
                        e.nowRegCnt -= 1
                    Sign.objects.filter(id=s.id).delete()
                    messages.add_message(request, messages.INFO, '取消成功！')
                elif s.exmStatus == 2:
                    messages.add_message(request, messages.INFO, '报名已审核通过，若要取消报名请联系管理员！')
            e.save()
    else:
        # messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect(
            'https://accounts.net9.org/api/authorize?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&redirect_uri=http://"+request.get_host+"/authorized')

    return HttpResponseRedirect('/events/' + Id + '/');


@csrf_exempt
def addevents(request):
    if request.method == "POST":
        if not request.POST['name']:
            messages.add_message(request, messages.INFO, "赛事名不能为空！")
            return render(request, "Events/addevents.html")
        checkbox = request.POST.getlist("checkbox")
        if len(checkbox) == 0:
            messages.add_message(request, messages.INFO, "请选择赛事类型！")
            return render(request, "Events/addevents.html")
        

        if int(request.POST['teammax']) < int(request.POST['teammin']):
            messages.add_message(request, messages.INFO, "团队人数有误！")
            return render(request, "Events/addevents.html")

        if not request.POST['time1']:
            messages.add_message(request, messages.INFO, "请填写全部时间！")
            return render(request, "Events/addevents.html")

        if not request.POST['time2']:
            messages.add_message(request, messages.INFO, "请填写全部时间！")
            return render(request, "Events/addevents.html")

        if not request.POST['time3']:
            messages.add_message(request, messages.INFO, "请填写全部时间！")
            return render(request, "Events/addevents.html")

        
        broadcast = request.POST.getlist("broadcast")
        if len(broadcast) > 0:
            messages.add_message(request, messages.INFO, "成功添加公告！")
            Broadcast.objects.create(title=request.POST['name']+" 已创建", detail=request.POST['name']+"即将开始！\n新的风暴已经出现！\n欢迎大家踊跃报名！\n 报名开始时间:"+request.POST['time1'], publisher=request.session['userid'])
            


        if Events.objects.create(name=request.POST['name'], desc=request.POST['detail'], teamMode=checkbox[0],
                                 teamMin=request.POST['teammin'], teamMax=request.POST['teammax'],
                                 maxRegCnt=request.POST['num'], timeRegSt=request.POST['time1'],
                                 timeRegEn=request.POST['time2'], timeEvnSt=request.POST['time3']):
            messages.add_message(request, messages.INFO, '成功添加赛事' + request.POST['name'] + '！')
            return HttpResponseRedirect('/events/')
    return render(request, "Events/addevents.html")


def gets2(i):
    if i == 1:
        return "即将开始"
    elif i == 2:
        return "正在报名"
    elif i == 3:
        return "报名已截止"
    elif i == 4:
        return "正在比赛"
    else:
        return "比赛已截止"


def gets3(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"
    else:
        return ""


def gets4(i):
    if i == 1:
        return "blue"
    elif i == 2:
        return "green"
    elif i == 3:
        return "red"
    elif i == 4:
        return "yellow"
    else:
        return "grey"


def qrcode(request):
    Id = request.session['eventsid']
    url = 'http://' + str(request.get_host()) + '/events/' + Id;
    code = pyqrcode.create(url)
    buff = io.BytesIO()
    code.png(buff, scale=8)
    image_data = buff.getvalue()
    return HttpResponse(image_data, content_type="image/png")



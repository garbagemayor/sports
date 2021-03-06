# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Users.models import Notification
import django.utils.timezone as timezone

import os,sys
import re

import pandas as pd
import xlsxwriter
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from HomePage.models import Events
from HomePage.models import Signs
from HomePage.models import Users
from HomePage.models import utcToLocal
from RegistrationRecord.forms import EditForm
from django.contrib import messages


def toUtf8WithNone(x):
    if x == None:
        return u"--"
    else:
        return unicode(x)


class RecordItem:
    """
    用来记录一堆信息，给registration_record.html使用
    """

    def __init__(self, record):
        user = Users.objects.get(id=record.userId)
        self.userIdSet = set([record.userId])
        # 报名的信息
        self.userId = record.userId
        self.eventId = record.eventId
        self.teamSize = record.teamSize
        self.timeRegStr = utcToLocal(record.timeReg).strftime("%Y-%m-%d %H:%M:%S")
        self.status = record.exmStatus
        self.statusStr = [u"", u"等待审核", u"审核通过", u"审核未通过"][self.status]
        self.statusToClass = [u"", u"info", u"success", u"warning", u"danger"][self.status]
        # 队长的信息

        self.captainName = toUtf8WithNone(user.name)
        self.captainFullname = toUtf8WithNone(user.fullname)
        # 报名用户的信息
        self.name = toUtf8WithNone(user.name)
        self.fullname = toUtf8WithNone(user.fullname)
        self.certification_type = [u"身份证", u"护照", u""][user.certification_type]
        self.certification_id = toUtf8WithNone(user.certification_id)
        self.mobile = toUtf8WithNone(user.mobile)
        self.classnumber = toUtf8WithNone(user.classnumber)
        self.email = toUtf8WithNone(user.email)
        self.student_number = toUtf8WithNone(user.student_number)
        self.room_address = toUtf8WithNone(user.room_address)
        self.cloth_size = toUtf8WithNone(user.cloth_size)
        self.gender = toUtf8WithNone(user.gender)
        self.degree = toUtf8WithNone(user.degree)
        # 队友的信息
        if record.teamSize > 1:
            teamMateList = re.findall(r'\d+', record.teamMate)
            for teamMateUserId in teamMateList:
                if int(teamMateUserId) in self.userIdSet:
                    continue
                self.userIdSet.add(int(teamMateUserId))
                user = Users.objects.get(id=int(teamMateUserId))
                self.name = self.name + "\n" + toUtf8WithNone(user.name)
                self.fullname = self.fullname + "\n" + toUtf8WithNone(user.fullname)
                self.certification_type = self.certification_type + "\n" +  [u"身份证", u"护照", u""][user.certification_type]
                self.certification_id = self.certification_id + "\n" + toUtf8WithNone(user.certification_id)
                self.mobile = self.mobile + "\n" + toUtf8WithNone(user.mobile)
                self.classnumber = self.classnumber + "\n" + toUtf8WithNone(user.classnumber)
                self.email = self.email + "\n" + toUtf8WithNone(user.email)
                self.student_number = self.student_number + "\n" + toUtf8WithNone(user.student_number)
                self.room_address = self.room_address + "\n" + toUtf8WithNone(user.room_address)
                self.cloth_size = self.cloth_size + "\n" + toUtf8WithNone(user.cloth_size)
                self.gender = self.gender + "\n" + toUtf8WithNone(user.gender)
                self.degree = self.degree + "\n" + toUtf8WithNone(user.degree)
        self.userIdSet = list(self.userIdSet)

    def printAll(self):
        print u'<class RegistrationRecord.views.RecordItem> {'
        print u'    ' + u'userIdSet = ' + unicode(self.userIdSet)
        print u'    ' + u'userId = ' + unicode(self.userId)
        print u'    ' + u'eventId = ' + unicode(self.eventId)
        print u'    ' + u'teamSize = ' + unicode(self.teamSize)
        print u'    ' + u'timeRegStr = ' + unicode(self.timeRegStr)
        print u'    ' + u'status = ' + unicode(self.status)
        print u'    ' + u'statusStr = ' + unicode(self.statusStr)
        print u'    ' + u'statusToClass = ' + unicode(self.statusToClass)
        if self.teamSize > 1:
            print u'    ' + u'captainName = ' + unicode(self.captainName)
            print u'    ' + u'captainFullname = ' + unicode(self.captainFullname)
        print u'    ' + u'name = ' + unicode(self.name)
        print u'    ' + u'fullname = ' + unicode(self.fullname)
        print u'    ' + u'certification_type = ' + unicode(self.certification_type)
        print u'    ' + u'certification_id = ' + unicode(self.certification_id)
        print u'    ' + u'mobile = ' + unicode(self.mobile)
        print u'    ' + u'classnumber = ' + unicode(self.classnumber)
        print u'    ' + u'email = ' + unicode(self.email)
        print u'    ' + u'student_number = ' + unicode(self.student_number)
        print u'    ' + u'room_address = ' + unicode(self.room_address)
        print u'    ' + u'cloth_size = ' + unicode(self.cloth_size)
        print u'    ' + u'gender = ' + unicode(self.gender)
        print u'    ' + u'degree = ' + unicode(self.degree)
        print u'}'

@csrf_exempt
def recordPage(request, event_id):
    event_id = int(event_id)
    # 当前赛事的信息
    event = Events.objects.get(id=event_id)
    request.session['eventname'] = event.name
    if request.method=="POST":
        EMAIL_FROM = '924486024@qq.com'
        print request.POST
        checkbox_list = request.POST.getlist("checked")
        passExamine = request.POST.getlist("passExamineSelector")
        emailOrNote = request.POST.getlist("emailOrNoteSelector")
        sendMessage = request.POST.getlist("sendMessageSelector")
        content = request.POST['content']
        print "checkbox_list", checkbox_list
        print "passExanime", passExamine
        print "emailOrNote", emailOrNote
        print "sendMessage", sendMessage
        print "content", content
        title = "已通过审核" if passExamine[0] == '1' else "未通过审核"
        title = event.name + "：" + title
        print title
        # 这个部分只操作数据库
        for checkbox_item in checkbox_list:
            captainId = int(checkbox_item.split('|')[0]);
            teammateIdStrList = re.findall(r'\d+', checkbox_item.split('|')[1])
            Signs.objects.filter(eventId=event_id,userId=captainId).update(exmStatus=2 if passExamine[0] == '1' else 3)
        # 这个部分只操作站内信
        if emailOrNote[0] == '1' or emailOrNote[0] == '3':
            for checkbox_item in checkbox_list:
                captainId = int(checkbox_item.split('|')[0]);
                teammateIdStrList = re.findall(r'\d+', checkbox_item.split('|')[1])
                if sendMessage == None or len(sendMessage) == 0 or sendMessage[0] == 1:
                    Notification.objects.create(
                        sender=request.session['username'],
                        senderId=request.session['userid'],
                        target=captainId,
                        title=title,
                        content=content)
                else:
                    for teammateIdStr in teammateIdStrList:
                        teammateId = int(teammateIdStr)
                        content_tmp = Users.objects.get(id=teammateId).name + content
                        Notification.objects.create(
                            sender=request.session['username'],
                            senderId=request.session['userid'],
                            target=teammateId,
                            title=title,
                            content=content)
        # 这个部分只操作邮件
        if emailOrNote[0] == '2' or emailOrNote[0] == '3':
            email_list = []
            for checkbox_item in checkbox_list:
                captainId = int(checkbox_item.split('|')[0]);
                teammateIdStrList = re.findall(r'\d+', checkbox_item.split('|')[1])
                if sendMessage == None or sendMessage[0] == 1:
                    email_list.append(Users.objects.get(id=captainId).email)
                else:
                    for teammateIdStr in teammateIdStrList:
                        teammateId = int(teammateIdStr)
                        email_list.append(Users.objects.get(id=teammateId).email)
            send_mail(title, content, EMAIL_FROM, email_list)
                 
        messages.add_message(request, messages.INFO, '审核成功')
    # 当前赛事的所有报名记录
    record_db_list = list(Signs.objects.filter(eventId=event_id))
    record_list = []
    for record_db in record_db_list:
        ri = RecordItem(record_db)
        record_list.append(ri)
    record_list_len = len(record_list)
    # 分页模块
    paginator=Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        record_list = paginator.page(page)
    except PageNotAnInteger:
        record_list = paginator.page(1)
    except EmptyPage:
        record_list = paginator.page(paginator.num_pages)
    form = EditForm()
    # 信息放在一起
    message_map = {}
    message_map['event'] = event
    message_map['record_list_len'] = record_list_len
    message_map['record_list'] = record_list
    message_map['form'] = form
    message_map['request'] = request
    return render(request, 'RegistrationRecord/registration_record.html', message_map)

# 文件传输迭代器
def file_iterator(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def recordDownloadCSV(request, event_id):
    event_id = int(event_id)
    # 当前赛事的信息
    event = Events.objects.get(id=event_id)
    # 当前赛事的所有报名记录
    record_db_list = list(Signs.objects.filter(eventId=event_id, exmStatus=2))
    record_list = []
    for record_db in record_db_list:
        ri = RecordItem(record_db)
        record_list.append(ri)
    # 生成文件
    abspath = os.path.abspath('.')
    relpath = str("/RegistrationRecord/templates/Temp/")
    if abspath.find("\\"):
        relpath = relpath.replace("/", "\\")
    if not os.path.exists(abspath + relpath):
        os.mkdir(abspath + relpath)
    file_name = str(abspath + relpath + "RecordList.csv")
    table_header = unicode(Events.objects.get(id=event_id).name) + u"的报名表"
    table_map = {
        u"姓名": [],
        u"性别": [],
        u"学号": [],
        u"身份证号": [],
        u"班级": [],
        u"手机号": [],
        u"邮箱": [],
        u"衣服尺码": [],
    } if event.teamMode == 0 else {
        u"队长": [],
        u"队员": [],
        u"性别": [],
        u"学号": [],
        u"身份证号": [],
        u"班级": [],
        u"手机号": [],
        u"邮箱": [],
        u"衣服尺码": [],
    }
    for record in record_list:
        if event.teamMode == 0:
            table_map[u"姓名"].append(toUtf8WithNone(record.fullname.replace("\n", "|")))
        else:
            table_map[u"队长"].append(toUtf8WithNone(record.captainFullname))
            table_map[u"队员"].append(toUtf8WithNone(record.fullname.replace("\n", "|")))
        table_map[u"性别"].append(toUtf8WithNone(record.gender.replace("\n", "|")))
        table_map[u"学号"].append(toUtf8WithNone(record.student_number.replace("\n", "|")))
        table_map[u"身份证号"].append(toUtf8WithNone(record.certification_id.replace("\n", "|")))
        table_map[u"班级"].append(toUtf8WithNone(record.classnumber.replace("\n", "|")))
        table_map[u"手机号"].append(toUtf8WithNone(record.mobile.replace("\n", "|")))
        table_map[u"邮箱"].append(toUtf8WithNone(record.email.replace("\n", "|")))
        table_map[u"衣服尺码"].append(toUtf8WithNone(record.cloth_size.replace("\n", "|")))
    dataFrame = pd.DataFrame(table_map)
    dataFrame.to_csv(file_name, encoding="utf-8", header=table_header, index=True, index_label=u'编号')

    # 传输下载
    import random
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = u'attachment;filename="table_%d.csv"' % (random.randint(0, 0x7fffffff))
    return response


def getUnicodeLength(str):
    len = 0
    for ch in str:
        try:
            ch.decode('ascii')
            len += 1
        except (UnicodeDecodeError, UnicodeEncodeError), e:
            len += 2
    return len

def writeExcelFile(teamMode ,table_header, record_list, file_name):
    # 打开一个Excel工作簿，新建一个sheet，如果对一个单元格重复操作，会引发异常，所以加上参数cell_overwrite_ok=True
    workbook = xlsxwriter.Workbook(file_name)
    sheet = workbook.add_worksheet(name=u'报名表')

    # 写列标
    fields = [
        u"编号",
        u"姓名",
        u"性别",
        u"学号",
        u"身份证号",
        u"班级",
        u"手机号",
        u"邮箱",
        u"衣服尺码",
    ] if teamMode == 0 else [
        u"编号",
        u"队长",
        u"队员",
        u"性别",
        u"学号",
        u"身份证号",
        u"班级",
        u"手机号",
        u"邮箱",
        u"衣服尺码",
    ]
    for j in range(len(fields)):
        sheet.write(1, j, u'%s' % fields[j])

    # 写表格标题，单元格合并的信息
    # sheet.write_merge(x, x + m, y, w + n, string, sytle)
    # x表示行，y表示列，m表示跨行个数，n表示跨列个数，string表示要写入的单元格内容，style表示单元格样式。其中，x，y，w，h，都是以0开始计算的。
    sheet.merge_range(0, 0, 0, len(fields) - 1, data=table_header)
    # sheet.write(0, 0 + 1, 0, 0 + 9, table_header)

    # 统计列宽
    column_width = []
    for j in range(len(fields)):
        column_width.append(len(fields[j]))

    # 写入数据
    n = len(record_list)
    for i in range(n):
        row_data = [
            toUtf8WithNone(i),
            record_list[i].fullname.replace("\n", ","),
            record_list[i].gender.replace("\n", ","),
            record_list[i].student_number.replace("\n", ","),
            record_list[i].certification_id.replace("\n", ","),
            record_list[i].classnumber.replace("\n", ","),
            record_list[i].mobile.replace("\n", ","),
            record_list[i].email.replace("\n", ","),
            record_list[i].cloth_size.replace("\n", ","),
        ]
        if teamMode == 1:
            row_data.insert(1, record_list[i].captainFullname)
        for j in range(len(fields)):
            sheet.write(i + 2, j, row_data[j])
            if column_width[j] < getUnicodeLength(row_data[j]):
                column_width[j] = getUnicodeLength(row_data[j])

    # 调整列宽
    for j in range(len(fields)):
        sheet.set_column(firstcol=j, lastcol=j, width=column_width[j] + 2)

    # 保存文件
    try:
        workbook.close()
        return True
    except IOError, e:
        return False

def recordDownloadXLSX(request, event_id):
    event_id = int(event_id)
    # 当前赛事的信息
    event = Events.objects.get(id=event_id)
    # 当前赛事的所有报名记录
    record_db_list = list(Signs.objects.filter(eventId=event_id, exmStatus=2))
    record_list = []
    for record_db in record_db_list:
        ri = RecordItem(record_db)
        record_list.append(ri)
    # 生成路径
    abspath = os.path.abspath('.')
    relpath = str("/RegistrationRecord/templates/Temp/")
    if abspath.find("\\"):
        relpath = relpath.replace("/", "\\")
    if not os.path.exists(abspath + relpath):
        os.mkdir(abspath + relpath)
    file_name = abspath + relpath + "RecordList.xlsx"
    # 生成文件
    table_header = unicode(Events.objects.get(id=event_id).name) + u"的报名表"
    r = writeExcelFile(event.teamMode ,table_header, record_list, file_name)
    if not r:   # 生成文件失败了
        messages.add_message(request, messages.INFO,
                             '生成报名表文件失败，可能是有个逗比在服务器上瞎搞')
    # 传输下载
    import random
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = u'attachment;filename="table_%d.xlsx"' % (random.randint(0, 0x7fffffff))
    return response

def confirm(request):
    result = "你好!\n    您报名参加的" + request.session['eventname']
    if request.POST['result'] == "True":
        result = result + "已通过审核!"
    else:
        result = result + "审核没有通过!"
    return HttpResponse(result)
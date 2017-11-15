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
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from HomePage.models import Events
from HomePage.models import Signs
from HomePage.models import Users
from .forms import EmailForm
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
        self.timeRegStr = record.timeReg.strftime("%Y-%m-%d %H:%M:%S")
        self.status = record.exmStatus
        self.statusStr = [u"", u"等待审核", u"审核通过", u"审核未通过"][self.status]
        self.statusToClass = [u"", u"info", u"success", u"error"][self.status]
        # 队长的信息
        if self.teamSize > 1:
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

@csrf_exempt
def recordPage(request, event_id):
    event_id = int(event_id)
    if request.method=="POST":
        checkbox_list=request.POST.getlist("checked")
        form = EmailForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data['title']
            c = form.cleaned_data['content']
            r = form.cleaned_data['result']
            for ii in checkbox_list:
                print ii, type(ii)
                for iii in re.findall(r'\d+', ii):
                    i = int(iii)
                    print i, type(i)
                    if r:
                        Signs.objects.filter(eventId=event_id,userId=i).update(exmStatus=2)
                    else:
                        Signs.objects.filter(eventId=event_id,userId=i).update(exmStatus=3)
                    Notification.objects.create(sender=request.session['userid'],
                        target=i, title=t, content=c, createTime=timezone.now())
        messages.add_message(request, messages.INFO, '审核成功')
    # 当前赛事的信息
    event = Events.objects.get(id=event_id)
    # 当前赛事的所有报名记录
    record_db_list = list(Signs.objects.filter(eventId=event_id))
    record_list = []
    for record_db in record_db_list:
        ri = RecordItem(record_db)
        record_list.append(ri)
    # 分页模块
    paginator=Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        record_list = paginator.page(page)
    except PageNotAnInteger:
        record_list = paginator.page(1)
    except EmptyPage:
        record_list = paginator.page(paginator.num_pages)
    form = EmailForm()
    # 信息柔和在一起
    message_map = {}
    message_map['event'] = event
    message_map['record_list'] = record_list
    message_map['form'] = form
    return render(request, 'RegistrationRecord/registration_record.html', message_map)

# 文件传输迭代器
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
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
            table_map[u"队长"].append(toUtf8WithNone(record.captainFullName))
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
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

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
    sheet.merge_range(0, 0, 0, len(fields), data=table_header)
    # sheet.write(0, 0 + 1, 0, 0 + 9, table_header)


    # 写入数据
    n = len(record_list)
    for i in range(n):
        j = 0           # 编号
        sheet.write(i + 2, j, toUtf8WithNone(i))
        if teamMode == 0:
            j += 1      # 姓名
            sheet.write(i + 2, j, record_list[i].fullname)
        else:
            j += 1      # 队长
            sheet.write(i + 2, j, record_list[i].captainFullName)
            j += 1      # 队员
            sheet.write(i + 2, j, record_list[i].fullname)
        j += 1          # 性别
        sheet.write(i + 2, j, record_list[i].gender)
        j += 1          # 学号
        sheet.write(i + 2, j, record_list[i].student_number)
        j += 1          # 身份证号
        sheet.write(i + 2, j, record_list[i].certification_id)
        j += 1          # 班级
        sheet.write(i + 2, j, record_list[i].classnumber)
        j += 1          # 手机号
        sheet.write(i + 2, j, record_list[i].mobile)
        j += 1          # 邮箱
        sheet.write(i + 2, j, record_list[i].email)
        j += 1          # 衣服尺码
        sheet.write(i + 2, j, record_list[i].cloth_size)

    # 保存文件
    workbook.close()

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
    writeExcelFile(event.teamMode ,table_header, record_list, file_name)
    # 传输下载
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def edit_email(request, event_id):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_title = form.cleaned_data['title']
            email_content = form.cleaned_data['content']
            EMAIL_FROM = '924486024@qq.com'
            email_list = []
            for obj in Signs.objects.filter(eventId=event_id, exmStatus=2):
                email_list.append(Users.objects.get(id=obj.userId).email)
            send_status = send_mail(email_title, email_content, EMAIL_FROM,
                                    email_list)
            if send_status:
                messages.add_message(request, messages.INFO, '发送成功')
                return HttpResponseRedirect('/record/' + str(event_id))
            messages.add_message(request, messages.INFO,
                    '发送失败,请检查目标邮箱是否正确')
            return render(request, 'RegistrationRecord/edit_email.html', {'form': form})
        messages.add_message(request, messages.INFO, '发送失败,请检查发送内容')
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})
    else:
        email_list = []
        for obj in Signs.objects.filter(eventId=event_id,exmStatus=2):
            email_list.append(Users.objects.get(id=obj.userId).email)
        form = EmailForm()
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})

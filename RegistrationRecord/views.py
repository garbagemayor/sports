# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HomePage.models import Events as MEvents
from HomePage.models import Sign as MSign
from HomePage.models import User as MUser

import os,sys

import pandas as pd
import xlwt, xlsxwriter

from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseRedirect

import django.utils.timezone as timezone

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt,csrf_protect

class RecordItem:
    '''
    用来记录一堆信息，给registration_record.html使用
    '''
    def __init__(self, record_db):
        self.record_id = record_db.id
        self.user_id = record_db.userid
        self.record_time = record_db.time
        # self.record_time = timezone.now
        user_db = MUser.objects.get(id=record_db.userid)
        self.user_name = user_db.name
        self.user_mobile = user_db.mobile
        self.user_fullname = user_db.fullname
        self.user_classnumber = user_db.classnumber
        self.user_email = user_db.email
        if record_db.status == 0:
            self.record_status = "审核未通过"
        elif record_db.status == 1:
            self.record_status = "等待审核"
        elif record_db.status == 2:
            self.record_status = "审核通过"

@csrf_exempt
def recordPage(request, event_id):
    if request.method=="POST":
        checkbox_list=request.POST.getlist("checked")
        for i in checkbox_list:
            MSign.objects.filter(id=i).update(status=2)
    event_id = int(event_id)
    message_map = {}
    # 当前赛事的信息
    event = MEvents.objects.get(id=event_id)
    message_map['event'] = event
    # 当前赛事的所有报名记录
    record_db_list = list(MSign.objects.filter(eventsid=event_id))
    record_list = []
    for record_db in record_db_list:
        record_list.append(RecordItem(record_db))
    # 分页模块
    paginator=Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        record_list = paginator.page(page)
    except PageNotAnInteger:
        record_list = paginator.page(1)
    except EmptyPage:
        record_list = paginator.page(paginator.num_pages)
    message_map['record_list'] = record_list
    return render(request, 'RegistrationRecord/registration_record.html', message_map)


def recordDownloadCSV(request, event_id):
    event_id = int(event_id)
    # 生成文件
    record_list = list(MSign.objects.filter(eventsid=event_id))
    abspath = os.path.abspath('.')
    file_name = str(abspath + "/RegistrationRecord/templates/Temp/RecordList.csv")
    recordid_list = []
    userid_list = []
    eventsid_list = []
    for record in record_list:
        recordid_list.append(str(record.id))
        userid_list.append(str(record.userid))
        eventsid_list.append(str(record.eventsid))
    dataFrame = pd.DataFrame({'recordid': recordid_list,
                              'userid': userid_list,
                              'eventsid': eventsid_list})
    dataFrame.to_csv(file_name)
    # 文件传输迭代器
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # 传输下载
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

'''
def getHeaderStyle():
    style = xlwt.XFStyle()

    # 设置字体
    font = xlwt.Font()
    font.name = 'Courier New'
    font.bold = True
    font.color_index = 000
    font.height = 300
    style.font = font

    # 设置单元格边框
    borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    borders.bottom = 6
    style.borders = borders

    # 设置单元格背景颜色
    pattern = xlwt.Pattern()
    # 设置其模式为实型
    pattern.pattern = pattern.SOLID_PATTERN
    # 设置单元格背景颜色
    pattern.pattern_fore_colour = 0xFFFF00
    style.pattern = pattern

    return style


def getContentStyle():
    style = xlwt.XFStyle()      # 初始化样式
    font = xlwt.Font()          # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = False
    font.color_index = 000
    font.height = 200
    style.font = font

    # 设置单元格边框
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    # style.borders = borders

    # 设置单元格背景颜色
    # pattern = xlwt.Pattern()
    # 设置其模式为实型
    # pattern.pattern = pattern.SOLID_PATTERN
    # 设置单元格背景颜色
    # pattern.pattern_fore_colour = 0x00
    # style.pattern = pattern

    return style
'''

def writeExcelFile(record_list, file_name):
    # 打开一个Excel工作簿，新建一个sheet，如果对一个单元格重复操作，会引发异常，所以加上参数cell_overwrite_ok=True
    workbook = xlsxwriter.Workbook(file_name)
    sheet = workbook.add_worksheet(name=u'报名表')

    # 写标题栏
    fields = ['recordid', 'userid', 'eventsid']
    for j in range(len(fields)):
        sheet.write(0, j, u'%s' % fields[j])

    # 单元格合并的信息
    # sheet.write_merge(x, x + m, y, w + n, string, sytle)
    # x表示行，y表示列，m表示跨行个数，n表示跨列个数，string表示要写入的单元格内容，style表示单元格样式。其中，x，y，w，h，都是以0开始计算的。

    # 写入数据
    for i in range(len(record_list)):
        sheet.write(i + 1, 0, u'%s' % record_list[i].id)
        sheet.write(i + 1, 1, u'%s' % record_list[i].userid)
        sheet.write(i + 1, 2, u'%s' % record_list[i].eventsid)

    # 保存文件
    workbook.close()

def recordDownloadXLSX(request, event_id):
    event_id = int(event_id)
    # 生成文件
    record_list = list(MSign.objects.filter(eventsid=event_id))
    abspath = os.path.abspath('.')
    file_name = abspath + "/RegistrationRecord/templates/Temp/RecordList.xlsx"
    writeExcelFile(record_list, file_name)
    # 文件传输迭代器
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # 传输下载
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

def edit_email(request, event_id):
    record_list = list(MSign.objects.filter(eventsid=event_id))
    email_list = []
    email_str = ""
    for record in record_list:
        email_list.append(MUser.objects.get(id=record.userid).email)
    for email in email_list:
        email_str = email_str + str(email) + "; "
    print email_str
    if (request.method == 'POST'):
        form = PostForm(request.POST)
        if form.is_valid():
            for email_addr in email_list:
                email_title = request.POST['title']
                email_content = request.POST['content']
                EMAIL_FROM = '924486024@qq.com'
                send_status = send_mail(email_title, email_content, EMAIL_FROM,
                        [email_addr])
            if send_status:
                return HttpResponseRedirect('/record/'+str(event_id))
    else:
        form = PostForm(initial={'addr': email_str, 'title': "报名成功",
            'content': "以下是赛事详情"})
        return render(request, 'RegistrationRecord/edit_email.html', {'form':
            form})

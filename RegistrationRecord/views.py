# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import pandas as pd
import xlsxwriter
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from HomePage.models import Events as MEvents
from HomePage.models import Signs as MSign
from HomePage.models import Users as MUser
from .forms import EmailForm


class RecordItem:
    """
    用来记录一堆信息，给registration_record.html使用
    """

    def __init__(self, record):
        self.record = record
        self.user = MUser.objects.get(id=record.userId)
        self.status = record.exmStatus
        self.timeRegStr = record.timeReg.strftime("%Y-%m-%d %H:%M:%S")
        if record.exmStatus == 1:
            self.statusStr = "等待审核"
            self.statusToClass = "info"
        elif record.exmStatus == 2:
            self.statusStr = "审核通过"
            self.statusToClass = "success"
        elif record.exmStatus == 3:
            self.statusStr = "审核未通过"
            self.statusToClass = "error"


def toUtf8WithNone(x):
    if x is None:
        return u"--"
    else:
        return unicode(x)


@csrf_exempt
def recordPage(request, event_id):
    if request.method == "POST":
        checkbox_list = request.POST.getlist("checked")
        for i in checkbox_list:
            MSign.objects.filter(eventId=event_id, userId=i).update(exmStatus=2)
        return HttpResponseRedirect('/edit_email/' + str(event_id))
    event_id = int(event_id)
    message_map = {}
    # 当前赛事的信息
    event = MEvents.objects.get(id=event_id)
    message_map['event'] = event
    # 当前赛事的所有报名记录
    record_db_list = list(MSign.objects.filter(eventId=event_id))
    record_list = []
    for record_db in record_db_list:
        ri = RecordItem(record_db)
        record_list.append(ri)
    # 分页模块
    paginator = Paginator(record_list, 10)
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
    sign_list = list(MSign.objects.filter(eventId=event_id, exmStatus=2))
    abspath = os.path.abspath('.')
    relpath = str("/RegistrationRecord/templates/Temp/")
    if abspath.find("\\"):
        relpath = relpath.replace("/", "\\")
    if not os.path.exists(abspath + relpath):
        os.mkdir(abspath + relpath)
    file_name = str(abspath + relpath + "RecordList.csv")
    table_header = unicode(MEvents.objects.get(id=event_id).name) + u"的报名表"
    table_map = {
        u"姓名": [],
        u"性别": [],
        u"学号": [],
        u"身份证号": [],
        u"班级": [],
        u"手机号": [],
        u"邮箱": [],
        u"衣服尺码": [],
    }
    for sign in sign_list:
        user = MUser.objects.get(id=sign.userId)
        table_map[u"姓名"].append(toUtf8WithNone(user.fullname))
        table_map[u"性别"].append(toUtf8WithNone(user.gender))
        table_map[u"学号"].append(toUtf8WithNone(user.student_number))
        table_map[u"身份证号"].append(toUtf8WithNone(user.certification_id))
        table_map[u"班级"].append(toUtf8WithNone(user.classnumber))
        table_map[u"手机号"].append(toUtf8WithNone(user.mobile))
        table_map[u"邮箱"].append(toUtf8WithNone(user.email))
        table_map[u"衣服尺码"].append(toUtf8WithNone(user.cloth_size))
    dataFrame = pd.DataFrame(table_map)
    dataFrame.to_csv(file_name, encoding="utf-8", header=table_header, index=True, index_label=u'编号')

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


def writeExcelFile(table_header, table_map, file_name):
    # 打开一个Excel工作簿，新建一个sheet，如果对一个单元格重复操作，会引发异常，所以加上参数cell_overwrite_ok=True
    workbook = xlsxwriter.Workbook(file_name)
    sheet = workbook.add_worksheet(name=u'报名表')

    # 写表格标题，单元格合并的信息
    # sheet.write_merge(x, x + m, y, w + n, string, sytle)
    # x表示行，y表示列，m表示跨行个数，n表示跨列个数，string表示要写入的单元格内容，style表示单元格样式。其中，x，y，w，h，都是以0开始计算的。
    sheet.merge_range(0, 0, 0, 8, data=table_header)
    # sheet.write(0, 0 + 1, 0, 0 + 9, table_header)

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
    ]
    for j in range(len(fields)):
        sheet.write(1, j, u'%s' % fields[j])

    # 写入数据
    n = len(table_map[u"姓名"])
    for i in range(n):
        sheet.write(i + 2, 0, toUtf8WithNone(i))
        sheet.write(i + 2, 1, toUtf8WithNone(table_map[u"姓名"][i]))
        sheet.write(i + 2, 2, toUtf8WithNone(table_map[u"性别"][i]))
        sheet.write(i + 2, 3, toUtf8WithNone(table_map[u"学号"][i]))
        sheet.write(i + 2, 4, toUtf8WithNone(table_map[u"身份证号"][i]))
        sheet.write(i + 2, 5, toUtf8WithNone(table_map[u"班级"][i]))
        sheet.write(i + 2, 6, toUtf8WithNone(table_map[u"手机号"][i]))
        sheet.write(i + 2, 7, toUtf8WithNone(table_map[u"邮箱"][i]))
        sheet.write(i + 2, 8, toUtf8WithNone(table_map[u"衣服尺码"][i]))

    # 保存文件
    workbook.close()


def recordDownloadXLSX(request, event_id):
    event_id = int(event_id)
    # 生成文件
    abspath = os.path.abspath('.')
    relpath = str("/RegistrationRecord/templates/Temp/")
    if abspath.find("\\"):
        relpath = relpath.replace("/", "\\")
    if not os.path.exists(abspath + relpath):
        os.mkdir(abspath + relpath)
    file_name = abspath + relpath + "RecordList.xlsx"
    table_header = unicode(MEvents.objects.get(id=event_id).name) + u"的报名表"
    table_map = {
        u"姓名": [],
        u"性别": [],
        u"学号": [],
        u"身份证号": [],
        u"班级": [],
        u"手机号": [],
        u"邮箱": [],
        u"衣服尺码": [],
    }
    for sign in MSign.objects.filter(eventId=event_id, exmStatus=2):
        user = MUser.objects.get(id=sign.userId)
        table_map[u"姓名"].append(toUtf8WithNone(user.fullname))
        table_map[u"性别"].append(toUtf8WithNone(user.gender))
        table_map[u"学号"].append(toUtf8WithNone(user.student_number))
        table_map[u"身份证号"].append(toUtf8WithNone(user.certification_id))
        table_map[u"班级"].append(toUtf8WithNone(user.classnumber))
        table_map[u"手机号"].append(toUtf8WithNone(user.mobile))
        table_map[u"邮箱"].append(toUtf8WithNone(user.email))
        table_map[u"衣服尺码"].append(toUtf8WithNone(user.cloth_size))
    writeExcelFile(table_header, table_map, file_name)

    # 文件传输迭代器
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, "rb") as f:
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
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_title = form.cleaned_data['title']
            email_content = form.cleaned_data['content']
            EMAIL_FROM = '924486024@qq.com'
            email_list = []
            for obj in MSign.objects.filter(eventId=event_id, exmStatus=2):
                email_list.append(MUser.objects.get(id=obj.userId).email)
            print email_list
            send_status = send_mail(email_title, email_content, EMAIL_FROM,
                                    email_list)
            if send_status:
                return HttpResponseRedirect('/record/' + str(event_id))
            return render(request, 'RegistrationRecord/edit_email.html', {'form': form})
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})
    else:
        form = EmailForm()
        return render(request, 'RegistrationRecord/edit_email.html', {'form': form})

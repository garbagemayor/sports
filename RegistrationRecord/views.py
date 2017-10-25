# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HomePage.models import Events as MEvents
from HomePage.models import Sign as MSign

import os,sys

import pandas as pd

from django.shortcuts import render
from django.http import StreamingHttpResponse

def recordPage(request, event_id):
    event_id = int(event_id)
    message_map = {}
    # 当前赛事的信息
    event = MEvents.objects.get(id=event_id)
    message_map['event'] = event
    # 当前赛事的所有报名记录
    record_list = list(MSign.objects.filter(eventsid=event_id))
    message_map['record_list'] = record_list
    return render(request, 'RegistrationRecord/registration_record.html', message_map)


def recordDownload(request, event_id):
    event_id = int(event_id)
    # 生成文件
    record_list = list(MSign.objects.filter(eventsid=event_id))
    abspath = os.path.abspath('.')
    file_name = abspath + "/RegistrationRecord/templates/Temp/RecordList.csv"
    recordid_list = []
    userid_list = []
    eventsid_list = []
    for record in record_list:
        recordid_list.append(record.id)
        userid_list.append(record.userid)
        eventsid_list.append(record.eventsid)
    pd.DataFrame({'recordid': recordid_list,
                  'userid': userid_list,
                  'eventsid': eventsid_list})
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


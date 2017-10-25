# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HomePage.models import Events as MEvents
from HomePage.models import Sign as MSign

import os,sys

from django.shortcuts import render
from django.http import StreamingHttpResponse

def recordPage(request, event_id):
    event_id = int(event_id)
    message_map = {}
    # ��ǰ���µ���Ϣ
    event = MEvents.objects.get(id=event_id)
    message_map['event'] = event
    # ��ǰ���µ����б�����¼
    record_list = list(MSign.objects.filter(eventsid=event_id))
    message_map['record_list'] = record_list
    return render(request, 'RegistrationRecord/registration_record.html', message_map)


def recordDownload(request, event_id):
    event_id = int(event_id)
    # �����ļ�
    record_list = MSign.objects.filter(eventsid=event_id)
    abspath = os.path.abspath('.')
    file_name = abspath + "/RegistrationRecord/templates/Temp/RecordList.csv"
    file = open(file_name, "w")
    for record in record_list:
        file.write("%d," % (record.id))
        file.write("%d," % (record.userid))
        file.write("%d\n" % (record.eventsid))
    file.close()
    # �ļ����������
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # ��������
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


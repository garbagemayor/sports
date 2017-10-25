# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HomePage.models import Events as MEvents
from HomePage.models import Sign as MSign

from django.shortcuts import render

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



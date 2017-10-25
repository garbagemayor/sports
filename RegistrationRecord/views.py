# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HomePage.models import Events as MEvents
from HomePage.models import Sign as MSign

from django.shortcuts import render

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



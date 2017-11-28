# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import IMG, Team
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


def team(request, team_id):
    obj = Team.objects.get(id=team_id)
    mmap = {}
    mmap['id'] = obj.id
    mmap['sport'] = obj.sport
    mmap['name'] = obj.name
    mmap['captain'] = obj.captain
    mmap['achievement'] = obj.achievement
    mmap['athlete'] = obj.athlete
    mmap['detail'] = obj.detail
    mmap['train'] = obj.train
    mmap['joinus'] = obj.joinus
    mmap['headline'] = obj.headline
    mmap['no_edit'] = True
    return render(request, "Manager/team.html", mmap)


def team_edit(request, team_id):
    obj = Team.objects.get(id=team_id)
    mmap = {}
    mmap['captain'] = obj.captain
    mmap['achievement'] = obj.achievement
    mmap['athlete'] = obj.athlete
    mmap['detail'] = obj.detail
    mmap['train'] = obj.train
    mmap['joinus'] = obj.joinus
    mmap['headline'] = obj.headline
    mmap['no_edit'] = False
    if request.POST:
        Team.objects.filter(id=team_id).update(
            captain=request.POST['captain'],
            achievement=request.POST['achievement'],
            athlete=request.POST['athlete'],
            detail=request.POST['detail'],
            train=request.POST['train'],
            joinus=request.POST['joinus'],
        )

        messages.add_message(request, messages.INFO, '修改成功！')
        return HttpResponseRedirect('/team')
    return render(request, "Manager/team.html", mmap)
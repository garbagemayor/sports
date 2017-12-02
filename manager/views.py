# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.shortcuts import render
from HomePage.models import IMG, Team
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.


def team(request, team_id):
    obj = Team.objects.get(id=team_id)
    mmap = {}
    mmap['team_add'] = obj.name
    mmap['celebrity_add'] = obj.name
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
    mmap['team_add'] = '系队信息编辑'
    mmap['celebrity_add'] = '名人信息编辑'
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
    mmap['no_edit'] = False
    if request.POST:
        print request.POST.get('headline')
        if request.POST.get('headline') != None:
            Team.objects.filter(cate=request.POST['cate']).update(headline=False)
            for obj in list(Team.objects.filter(cate=request.POST['cate'])):
                IMG.objects.filter(imgtype=obj.id).update(headline=False)
            IMG.objects.filter(imgtype=team_id).update(headline=True)
            headline = True
        else:
            headline = False
        Team.objects.filter(id=team_id).update(
            name=request.POST['name'],
            captain=request.POST['captain'],
            achievement=request.POST['achievement'],
            athlete=request.POST['athlete'],
            detail=request.POST['detail'],
            train=request.POST['train'],
            joinus=request.POST['joinus'],
            headline=headline,
        )

        messages.add_message(request, messages.INFO, '修改成功！')
        return HttpResponseRedirect('/team/')
    return render(request, "Manager/team.html", mmap)

def team_add(request):
    mmap = {}
    mmap['team_add'] = '添加系队'
    mmap['celebrity_add'] = '添加名人'
    mmap['sport'] = '项目'
    mmap['name'] = '官方名称'
    mmap['captain'] = '队长'
    mmap['achievement'] = '战绩'
    mmap['athlete'] = '传奇运动员'
    mmap['detail'] = '介绍'
    mmap['train'] = '训练计划'
    mmap['joinus'] = '加入我们'
    mmap['headline'] = False
    mmap['no_edit'] = False
    mmap['id'] = len(list(Team.objects.filter())) + 1
    if request.POST:
        print "in post"
        print request.POST.get('headline')
        if request.POST.get('headline') != None:
            Team.objects.filter(cate=request.POST['cate']).update(headline=False)
            for obj in list(Team.objects.filter(cate=request.POST['cate'])):
                IMG.objects.filter(imgtype=obj.id).update(headline=False)
            IMG.objects.filter(imgtype=team_id).update(headline=True)
            headline = True
        else:
            headline = False
        g = Team.objects.create(
            cate=request.POST['cate'],
            sport=request.POST['sport'],
            name=request.POST['name'],
            captain=request.POST['captain'],
            achievement=request.POST['achievement'],
            athlete=request.POST['athlete'],
            detail=request.POST['detail'],
            train=request.POST['train'],
            joinus=request.POST['joinus'],
            headline=headline,
        )
        messages.add_message(request, messages.INFO, '添加成功！')
        return HttpResponseRedirect('/team/')
    return render(request, "Manager/team.html", mmap)

def team_remove(request):
    checkbox_list = request.POST['idlist']
    for checked_item in re.findall(r'\d+', checkbox_list):
        Team.objects.filter(id=int(checked_item)).delete()
    return HttpResponse('ok')

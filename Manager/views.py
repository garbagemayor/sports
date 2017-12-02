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
    mmap['name1'] = obj.name
    mmap['captain'] = obj.captain
    mmap['achievement'] = obj.achievement
    mmap['athlete'] = obj.athlete
    mmap['detail'] = obj.detail
    mmap['detail1'] = obj.detail
    mmap['train'] = obj.train
    mmap['joinus'] = obj.joinus
    mmap['headline'] = obj.headline
    mmap['headline1'] = obj.headline
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
    mmap['name1'] = obj.name
    mmap['captain'] = obj.captain
    mmap['achievement'] = obj.achievement
    mmap['athlete'] = obj.athlete
    mmap['detail'] = obj.detail
    mmap['detail1'] = obj.detail
    mmap['train'] = obj.train
    mmap['joinus'] = obj.joinus
    mmap['headline'] = obj.headline
    mmap['headline1'] = obj.headline
    mmap['no_edit'] = False
    if request.POST:
        cate = request.POST.get('cate')
        print cate
        if int(cate) == 1: # 系队
            print 'team'
            headline = request.POST.get('headline')
            name = request.POST['name']
            detail = request.POST['detail']
            print headline, name, detail
        else: # 名人
            print 'celebrity'
            headline = request.POST.get('headline1')
            name = request.POST['name1']
            detail = request.POST['detail1']
            print headline, name, detail
        print headline, name, detail, request
        if headline != None:
            # 从主页撤回所有系队或名人
            Team.objects.filter(cate=request.POST['cate']).update(headline=False)
            for obj in list(Team.objects.filter(cate=request.POST['cate'])):
                IMG.objects.filter(imgtype=obj.id).update(headline=False)

            # 把选中队伍的图片放到首页
            IMG.objects.filter(imgtype=team_id).update(headline=True)
            headline = True
        else:
            headline = False
        
        # 为新加入图片添加类型名称
        IMG.objects.filter(imgtype=team_id).update(imgtypename=name)
        Team.objects.filter(id=team_id).update(
            sport=request.POST['sport'],
            name=name,
            captain=request.POST['captain'],
            achievement=request.POST['achievement'],
            athlete=request.POST['athlete'],
            detail=detail,
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
    mmap['name1'] = '官方名称'
    mmap['captain'] = '队长'
    mmap['achievement'] = '战绩'
    mmap['athlete'] = '传奇运动员'
    mmap['detail'] = '介绍'
    mmap['detail1'] = '介绍'
    mmap['train'] = '训练计划'
    mmap['joinus'] = '加入我们'
    mmap['headline'] = False
    mmap['headline1'] = False
    mmap['no_edit'] = False
    mmap['id'] = len(list(Team.objects.filter())) - 4
    team_id = len(list(Team.objects.filter())) - 4
    if request.POST:
        cate = request.POST.get('cate')
        print cate
        if int(cate) == 1: # 系队
            print 'team add'
            headline = request.POST.get('headline')
            name = request.POST['name']
            detail = request.POST['detail']
            print headline, name, detail
        else: # 名人
            print 'celebrity add'
            headline = request.POST.get('headline1')
            name = request.POST['name1']
            detail = request.POST['detail1']
            print headline, name, detail
        if headline != None:
            # 从主页撤回所有系队或名人
            Team.objects.filter(cate=cate).update(headline=False)
            for obj in list(Team.objects.filter(cate=cate)):
                IMG.objects.filter(imgtype=obj.id).update(headline=False)
            
            # 把选中队伍的图片放到首页
            IMG.objects.filter(imgtype=team_id).update(headline=True)
            headline = True
        else:
            headline = False
        print headline, name, detail
        # 为新加入图片添加类型名称
        IMG.objects.filter(imgtype=team_id).update(imgtypename=name)
        Team.objects.create(
            cate=request.POST['cate'],
            sport=request.POST['sport'],
            name=name,
            captain=request.POST['captain'],
            achievement=request.POST['achievement'],
            athlete=request.POST['athlete'],
            detail=detail,
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
        IMG.objects.filter(imgtype=int(checked_item)).update(imgtype=0)
    return HttpResponse('remove')

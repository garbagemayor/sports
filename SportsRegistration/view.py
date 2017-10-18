from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt,csrf_protect


def HomePageView(request):
    return render(request, "HomePage/homepage.html")

def EventsView(request):
    return render(request, "Events/events.html")

def UsersView(request):
    return render(request, "Users/users.html")

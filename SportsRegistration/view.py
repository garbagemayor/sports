from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from HomePage.models import IMG


def HomePageView(request):
    print request.method
    return render(request, "HomePage/newhomepage.html")

def EventsView(request):
    print request.method
    return render(request, "Events/events.html")

def UsersView(request):
    print request.method
    return render(request, "Users/users.html")

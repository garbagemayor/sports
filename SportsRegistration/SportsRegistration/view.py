from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def firstView(request):
    return render(request, "index.html")

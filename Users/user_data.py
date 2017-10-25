from django.http import HttpResponse
from  django.shortcuts import render
from  django.views.decorators import csrf

def change_code(request):
    ctx = {}
    if request.POST:
            ctx['rlt'] = request.POST['old_password']
    print ctx
    return render(request, "Users/users.html", ctx);
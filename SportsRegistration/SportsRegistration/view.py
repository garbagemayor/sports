from django.http import HttpResponse

def firstView(request):
    return HttpResponse("My First View")
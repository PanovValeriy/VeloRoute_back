from django.shortcuts import render

from core.crud import addVisit


def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    addVisit(ip)
    return render(request, template_name='index.html')

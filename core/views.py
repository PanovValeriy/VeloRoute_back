from django.shortcuts import render

from core.constants import MODULE_CORE
from core.crud import addVisit, addView


def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    addVisit(ip)
    addView(MODULE_CORE)
    return render(request, template_name='index.html')

from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from core.constants import MODULE_CORE
from core.crud import addVisit, addView


@permission_classes([AllowAny])
def index(request):
    code = request.GET.get('code', '')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    addVisit(ip)
    if not code:
        addView(MODULE_CORE)
    return render(request, template_name='index.html')

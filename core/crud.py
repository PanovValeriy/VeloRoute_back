import operator

from django.db.models import Q

from core.models import Route, Report, Event


def readRouteList(search='', length=''):
    q = Q()
    if search != '':
        q &= operator.or_(operator.or_(Q(name__icontains=search), Q(description__icontains=search)), Q(pointList__icontains=search))
    lengthInt = 0
    if length != '':
        znak = length[0]
        try:
            lengthInt = int(length[1:])
        except:
            lengthInt = 0
        if znak not in '<=>':
            lengthInt = 0
    if lengthInt != 0:
        if znak == '<':
            q &= Q(length__lte=lengthInt)
        elif znak == '>':
            q &= Q(length__gte=lengthInt)
        elif znak == '=':
            q &= Q(length=lengthInt)

    result = Route.objects.filter(q)
    return result


def readRoute(id):
    try:
        result = Route.objects.get(pk=id)
    except:
        result = None
    return result


def readReportList():
    result = Report.objects.all()
    return result


def readReport(id):
    try:
        result = Report.objects.get(pk=id)
    except:
        result = None
    return result


def readEventList():
    result = Event.objects.all()
    return result


def readEvent(id):
    try:
        result = Event.objects.get(pk=id)
    except:
        result = None
    return result

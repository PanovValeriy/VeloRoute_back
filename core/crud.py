import datetime
import operator

from django.db.models import Q

from core.libs import ip2int
from core.models import Route, Report, Event, VisitCount


def readRouteList(search='', length=''):
    q = Q(status=2)
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
        if result.status == 0:
            result = None
    except:
        result = None
    return result


def readReportList():
    q = Q(status=2)
    result = Report.objects.filter(q)
    return result


def readReport(id):
    try:
        result = Report.objects.get(pk=id)
        if result.status == 0:
            result = None
    except:
        result = None
    return result


def readEventList():
    q = Q(status=2)
    result = Event.objects.filter(q)
    return result


def readEvent(id):
    try:
        result = Event.objects.get(pk=id)
        if result.status == 0:
            result = None
    except:
        result = None
    return result


def addVisit(ip):
    try:
        recVisitCount = VisitCount.objects.filter(date=datetime.date.today(), ip=ip2int(ip))[0]
        recVisitCount.count += 1
        recVisitCount.save()
    except:
        recVisitCount = VisitCount(ip=ip2int(ip), date=datetime.date.today(), count=1)
        recVisitCount.save()

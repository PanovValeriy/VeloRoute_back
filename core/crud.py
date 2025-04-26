import datetime
from django.utils import timezone
import operator
from django.db.models import Q
from core.constants import STATUS_PUBLIC
from core.libs import ip2int
from core.models import Route, Report, Event, VisitCount
from core.serializers import EventSerializer, RouteSerializer, ReportSerializer


def readRouteList(search='', length='', complexity=0, sort=''):
    # Фильтр по статусу
    q = Q(status=STATUS_PUBLIC)
    # Фильтр по тексту
    if search != '':
        q &= operator.or_(operator.or_(Q(name__icontains=search), Q(description__icontains=search)), Q(pointList__icontains=search))
    # Фильтр по протяженности
    if length != '':
        lengthStart, lengthEnd = list(map(int, length.split(',')))
    else:
        lengthStart, lengthEnd = (0, 0)
    if lengthStart > 0:
        q &= Q(length__gte=lengthStart)
    if lengthEnd > 0:
        q &= Q(length__lte=lengthEnd)
    # Фильтр по сложности
    if complexity != 0:
        q &= Q(complexity_id=complexity)

    # Сортировка
    order = ''
    if sort != '':
        if sort.find(':') != -1:
            sortField, sortNapr = sort.split(':')
        else:
            sortField = sort
            sortNapr = ''
        if sortField in {'name', 'length', 'dateCreate', 'dateUpdate'}:
            order = sortField
        if order != '' and sortNapr == 'desc':
            order = '-' + order
    if order == '':
        order = 'name'
    result = Route.objects.filter(q).order_by(order)
    return result


def readRoute(id):
    try:
        result = Route.objects.get(pk=id)
        if result.status < 2:
            result = None
    except:
        result = None
    return result


def readReportList(search='', sort='', routeId=0, eventId=0):
    # Фильтр по статусу
    q = Q(status=STATUS_PUBLIC)
    # Фильтр по тексту
    if search != '':
        q &= operator.or_(Q(name__icontains=search), Q(body__icontains=search))
    # Фильтр по маршруту
    if routeId != 0:
        q &= Q(route_id=routeId)
    # Фильтр по событию
    if eventId != 0:
        q &= Q(event_id=eventId)

    # Сортировка
    order = ''
    if sort != '':
        if sort.find(':') != -1:
            sortField, sortNapr = sort.split(':')
        else:
            sortField = sort
            sortNapr = ''
        if sortField in {'name', 'date', 'dateCreate', 'dateUpdate'}:
            order = sortField
        if order != '' and sortNapr == 'desc':
            order = '-' + order
    if order == '':
        order = 'name'

    result = Report.objects.filter(q).order_by(order)
    return result


def readReport(id):
    try:
        result = Report.objects.get(pk=id)
        if result.status < 2:
            result = None
    except:
        result = None
    return result


def readEventList(search='', hideArchive=False, sort='', routeId=0):
    # Фильтр по статусу
    q = Q(status=STATUS_PUBLIC)
    # Фильтр по строке
    if search != '':
        q &= operator.or_(Q(name__icontains=search), Q(description__icontains=search))
    # Фильтр по активности
    if hideArchive:
        q &= Q(startDateTime__gte=timezone.now())
    # Фильтр по маршруту
    if routeId != 0:
        q &= Q(route_id=routeId)

    # Сортировка
    order = ''
    if sort != '':
        if sort.find(':') != -1:
            sortField, sortNapr = sort.split(':')
        else:
            sortField = sort
            sortNapr = ''
        if sortField in {'name', 'startDateTime', 'dateCreate', 'dateUpdate'}:
            order = sortField
        if order != '' and sortNapr == 'desc':
            order = '-' + order
    if order == '':
        order = '-startDateTime'

    result = Event.objects.filter(q).order_by(order)
    return result


def readEvent(id):
    try:
        result = Event.objects.get(pk=id)
        if result.status < 2:
            result = None
    except:
        result = None
    return result


def readNewsList(count=5, operation=0):

    def findId(typeDoc, id):
        for news in newsList:
            if (news['type'] == typeDoc) and (news['id'] == id):
                return True
        return False

    newsList = []
    routeCreateList = Route.objects.filter(status=STATUS_PUBLIC).order_by('-dateCreate')[:count]
    reportCreateList = Report.objects.filter(status=STATUS_PUBLIC).order_by('-dateCreate')[:count]
    eventCreateList = Event.objects.filter(status=STATUS_PUBLIC).order_by('-dateCreate')[:count]
    routeUpdateList = Route.objects.filter(status=STATUS_PUBLIC).order_by('-dateUpdate')[:count]
    reportUpdateList = Report.objects.filter(status=STATUS_PUBLIC).order_by('-dateUpdate')[:count]
    eventUpdateList = Event.objects.filter(status=STATUS_PUBLIC).order_by('-dateUpdate')[:count]

    routeCreateRecNo = 0
    reportCreateRecNo = 0
    eventCreateRecNo = 0
    routeUpdateRecNo = 0
    reportUpdateRecNo = 0
    eventUpdateRecNo = 0
    i = 0
    while i < count:
        dateCreate = max(eventCreateList[eventCreateRecNo].dateCreate, routeCreateList[routeCreateRecNo].dateCreate, reportCreateList[reportCreateRecNo].dateCreate)
        dateUpdate = max(eventUpdateList[eventUpdateRecNo].dateUpdate, routeUpdateList[routeUpdateRecNo].dateUpdate, reportUpdateList[reportUpdateRecNo].dateUpdate)
        dateMax = max(dateCreate, dateUpdate)
        if operation == 1:
            dateMax = dateCreate
        elif operation == 2:
            dateMax = dateUpdate
        if operation in (0, 1) and dateMax == dateCreate:
            if eventCreateList[eventCreateRecNo].dateCreate == dateMax:
                if not findId(3, eventCreateList[eventCreateRecNo].id):
                    newsList.append({
                        'oper': 1,
                        'type': 3,
                        'id': eventCreateList[eventCreateRecNo].id,
                        'name': eventCreateList[eventCreateRecNo].name,
                        'record': EventSerializer(eventCreateList[eventCreateRecNo]).data,
                    })
                    i += 1
                eventCreateRecNo += 1
            elif routeCreateList[routeCreateRecNo].dateCreate == dateMax:
                if not findId(1, routeCreateList[routeCreateRecNo].id):
                    newsList.append({
                        'oper': 1,
                        'type': 1,
                        'id': routeCreateList[routeCreateRecNo].id,
                        'name': routeCreateList[routeCreateRecNo].name,
                        'record': RouteSerializer(routeCreateList[routeCreateRecNo]).data,
                    })
                    i += 1
                routeCreateRecNo += 1
            elif reportCreateList[reportCreateRecNo].dateCreate == dateMax:
                if not findId(2, reportCreateList[reportCreateRecNo].id):
                    newsList.append({
                        'oper': 1,
                        'type': 2,
                        'id': reportCreateList[reportCreateRecNo].id,
                        'name': reportCreateList[reportCreateRecNo].name,
                        'record': ReportSerializer(reportCreateList[reportCreateRecNo]).data,
                    })
                    i += 1
                reportCreateRecNo += 1
        elif operation in (0, 2) and dateMax == dateUpdate:
            if eventUpdateList[eventUpdateRecNo].dateUpdate == dateMax:
                if not findId(3, eventUpdateList[eventUpdateRecNo].id):
                    newsList.append({
                        'oper': 2,
                        'type': 3,
                        'id': eventUpdateList[eventUpdateRecNo].id,
                        'name': eventUpdateList[eventUpdateRecNo].name,
                        'record': EventSerializer(eventUpdateList[eventUpdateRecNo]).data,
                    })
                    i += 1
                eventUpdateRecNo += 1
            elif routeUpdateList[routeUpdateRecNo].dateUpdate == dateMax:
                if not findId(1, routeUpdateList[routeUpdateRecNo].id):
                    newsList.append({
                        'oper': 2,
                        'type': 1,
                        'id': routeUpdateList[routeUpdateRecNo].id,
                        'name': routeUpdateList[routeUpdateRecNo].name,
                        'record': RouteSerializer(routeUpdateList[routeUpdateRecNo]).data,
                    })
                    i += 1
                routeUpdateRecNo += 1
            elif reportUpdateList[reportUpdateRecNo].dateUpdate == dateMax:
                if not findId(2, reportUpdateList[reportUpdateRecNo].id):
                    newsList.append({
                        'oper': 2,
                        'type': 2,
                        'id': reportUpdateList[reportUpdateRecNo].id,
                        'name': reportUpdateList[reportUpdateRecNo].name,
                        'record': ReportSerializer(reportUpdateList[reportUpdateRecNo]).data,
                    })
                    i += 1
                reportUpdateRecNo += 1
    return newsList


def addVisit(ip):
    try:
        recVisitCount = VisitCount.objects.filter(date=datetime.date.today(), ip=ip2int(ip))[0]
        recVisitCount.count += 1
        recVisitCount.save()
    except:
        recVisitCount = VisitCount(ip=ip2int(ip), date=datetime.date.today(), count=1)
        recVisitCount.save()

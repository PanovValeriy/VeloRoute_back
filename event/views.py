from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.constants import STATUS_PUBLIC, STATUS_HIDE
from core.crud import readEventList, readEvent
from core.libs import calcCodeTrue
from core.serializers import EventListSerializer, EventSerializer


@api_view(['GET'])
def view_event_list(request):
    search = request.GET.get('search', '')
    hideArchive = request.GET.get('hideArchive', '') == 'true'
    sort = request.GET.get('sort', '')
    routeId = int(request.GET.get('routeId', 0))
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))

    eventList = readEventList(search, hideArchive, sort, routeId)
    recCount = eventList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit

    responseEventList = EventListSerializer(eventList, many=True).data[startRec:endRec]
    return Response({'recCount': recCount, 'eventList': responseEventList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_event(request, pk):
    event = readEvent(pk)
    code = request.GET.get('code', '')
    code_true = calcCodeTrue(pk, 3)
    if event:
        responseEvent = EventSerializer(event).data
        if event.status == STATUS_PUBLIC or (event.status == STATUS_HIDE and code == code_true):
            return Response(responseEvent, status=status.HTTP_200_OK)
    return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)

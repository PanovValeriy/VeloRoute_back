from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.crud import readEventList, readEvent
from core.serializers import EventListSerializer, EventSerializer


@api_view(['GET'])
def view_event_list(request):
    eventList = readEventList()
    recCount = eventList.count()
    responseEventList = EventListSerializer(eventList, many=True).data
    return Response({'recCount': recCount, 'eventList': responseEventList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_event(request, pk):
    event = readEvent(pk)
    if event is None:
        return Response({'error', 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    responseEvent = EventSerializer(event).data
    return Response(responseEvent, status=status.HTTP_200_OK)
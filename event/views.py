from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.constants import STATUS_PUBLIC, STATUS_HIDE, MODULE_EVENT, USER_STATUS_ACTIVE
from core.crud import readEventList, readEvent, addView, replaceTags, readEventFirst, like_toggle, event_member_toggle
from core.libs import calcCodeTrue
from core.serializers import EventListSerializer, EventSerializer, EventNotAuthSerializer
from user.crud import findUserLogin, checkUserStatus


@api_view(['GET'])
@permission_classes([AllowAny])
def view_event_list(request):
    search = request.GET.get('search', '')
    hideArchive = request.GET.get('hideArchive', '') == 'true'
    sort = request.GET.get('sort', '')
    routeId = int(request.GET.get('routeId', 0))
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))

    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    eventList = readEventList(search, hideArchive, sort, routeId, idUser)
    recCount = eventList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit

    responseEventList = EventListSerializer(eventList, many=True).data[startRec:endRec]
    return Response({'recCount': recCount, 'eventList': responseEventList}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_event(request, pk):

    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    event = readEvent(pk, idUser)
    code = request.GET.get('code', '')
    code_true = calcCodeTrue(pk, 3)
    if event:
        event.description = replaceTags(event.description)
        responseEvent = EventSerializer(event).data if idUser != 0 else EventNotAuthSerializer(event).data
        if event.status == STATUS_PUBLIC or (event.status == STATUS_HIDE and code == code_true):
            if not code:
                addView(MODULE_EVENT, event.id)
            return Response(responseEvent, status=status.HTTP_200_OK)
    return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_event_first(request):

    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    event = readEventFirst(idUser)
    if event == None:
        return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)
    responseEvent = EventListSerializer(event).data
    return Response(responseEvent, status = status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_event_member_toggle(request, pk):
    login = request.user.username
    loginStatus = checkUserStatus(login)
    if loginStatus['status'] == 'error':
        return Response(
            {'detail': loginStatus['message']},
            status=status.HTTP_401_UNAUTHORIZED
        )
    result = event_member_toggle(pk, loginStatus['user'].id)
    if result['status'] == 'success':
        event = readEvent(pk, loginStatus['user'].id)
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': result['message']}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_event_like_toggle(request, pk):
    login = request.user.username
    loginStatus = checkUserStatus(login)
    if loginStatus['status'] == 'error':
        return Response(
            {'detail': loginStatus['message']},
            status=status.HTTP_401_UNAUTHORIZED
        )
    result = like_toggle(MODULE_EVENT, pk, loginStatus['user'].id)
    if result['status'] == 'success':
        event = readEvent(pk, loginStatus['user'].id)
        return Response({'event': EventSerializer(event).data}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': result['message']}, status=status.HTTP_400_BAD_REQUEST)

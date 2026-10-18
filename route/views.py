from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.constants import STATUS_PUBLIC, STATUS_HIDE, MODULE_ROUTE, USER_STATUS_ACTIVE
from core.crud import readRouteList, readRoute, addView, replaceTags, readRouteListRandom, like_toggle
from core.libs import calcCodeTrue
from core.serializers import RouteListSerializer, RouteSerializer
from user.crud import findUserLogin, checkUserStatus


@api_view(['GET'])
@permission_classes([AllowAny])
def view_route_list(request):
    search = request.GET.get('search', '')
    length = request.GET.get('length', '')
    complexity = int(request.GET.get('complexity', '0'))
    sort = request.GET.get('sort', '')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id
    routeList = readRouteList(search, length, complexity, sort, idUser)
    recCount = routeList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit
    responseRouteList = RouteListSerializer(routeList, many=True).data[startRec:endRec]
    return Response({'recCount': recCount, 'routeList': responseRouteList}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_route(request, pk):
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    route = readRoute(pk, idUser)
    code = request.GET.get('code', '')
    code_true = calcCodeTrue(pk, 1)
    if route:
        route.description = replaceTags(route.description)
        responseRoute = RouteSerializer(route).data
        if route.status == STATUS_PUBLIC or (route.status == STATUS_HIDE and code == code_true):
            if not code:
                addView(MODULE_ROUTE, route.id)
            return Response(responseRoute, status=status.HTTP_200_OK)
    return Response({'error': 'Маршрут не найден'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_route_list_random(request, count):
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    routeList = readRouteListRandom(count, idUser)
    responseRouteList = RouteListSerializer(routeList, many=True).data
    return Response({'recCount': routeList.count(), 'routeList': responseRouteList}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_route_like_toggle(request, pk):
    login = request.user.username
    loginStatus = checkUserStatus(login)
    if loginStatus['status'] == 'error':
        return Response(
            {'detail': loginStatus['message']},
            status=status.HTTP_401_UNAUTHORIZED
        )
    result = like_toggle(MODULE_ROUTE, pk, loginStatus['user'].id)
    if result['status'] == 'success':
        return Response({'detail': result['message']}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': result['message']}, status=status.HTTP_400_BAD_REQUEST)

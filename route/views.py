from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.crud import readRouteList, readRoute
from core.serializers import RouteListSerializer, RouteSerializer


def routes(request):
    return render(request, template_name='routes.html')


@api_view(['GET'])
def view_route_list(request):
    search = request.GET.get('search', '')
    length = request.GET.get('length', '')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))
    routeList = readRouteList(search, length)
    recCount = routeList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit
    responseRouteList = RouteListSerializer(routeList, many=True).data[startRec:endRec]
    return Response({'recCount': recCount, 'routeList': responseRouteList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_route(request, pk):
    route = readRoute(pk)
    if route:
        responseRoute = RouteSerializer(route).data
        return Response(responseRoute, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Маршрут не найден'}, status=status.HTTP_404_NOT_FOUND)

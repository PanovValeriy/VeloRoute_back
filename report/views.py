from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.crud import readReportList, readReport
from core.serializers import ReportListSerializer, ReportSerializer


@api_view(['GET'])
def view_report_list(request):
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    routeId = int(request.GET.get('routeId', 0))
    eventId = int(request.GET.get('eventId', 0))
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))

    reportList = readReportList(search, sort, routeId, eventId)

    recCount = reportList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit
    responseReportList = ReportListSerializer(reportList, many=True).data[startRec:endRec]
    return Response({'recCount': reportList.count(), 'reportList': responseReportList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_report(request, pk):
    report = readReport(pk)
    if report is None:
        return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    responseReport = ReportSerializer(report).data
    return Response(responseReport, status=status.HTTP_200_OK)

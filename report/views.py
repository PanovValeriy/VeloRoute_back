from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.crud import readReportList, readReport
from core.serializers import ReportListSerializer, ReportSerializer


@api_view(['GET'])
def view_report_list(request):
    reportList = readReportList()
    responseReportList = ReportListSerializer(reportList, many=True).data
    return Response({'recCount': reportList.count(), 'reportList': responseReportList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_report(request, pk):
    report = readReport(pk)
    if report is None:
        return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    responseReport = ReportSerializer(report).data
    return Response(responseReport, status=status.HTTP_200_OK)

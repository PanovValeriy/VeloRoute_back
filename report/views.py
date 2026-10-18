from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.constants import STATUS_PUBLIC, STATUS_HIDE, MODULE_REPORT, USER_STATUS_ACTIVE
from core.crud import readReportList, readReport, addView, replaceTags, readReportListRandom, like_toggle
from core.libs import calcCodeTrue
from core.serializers import ReportListSerializer, ReportSerializer
from user.crud import findUserLogin, checkUserStatus


@api_view(['GET'])
@permission_classes([AllowAny])
def view_report_list(request):
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    routeId = int(request.GET.get('routeId', 0))
    eventId = int(request.GET.get('eventId', 0))
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))

    reportList = readReportList(search, sort, routeId, eventId, idUser)

    recCount = reportList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit
    responseReportList = ReportListSerializer(reportList, many=True).data[startRec:endRec]
    return Response({'recCount': reportList.count(), 'reportList': responseReportList}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_report(request, pk):
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    report = readReport(pk, idUser)
    code = request.GET.get('code', '')
    code_true = calcCodeTrue(pk, 2)
    if report:
        report.body = replaceTags(report.body)
        responseReport = ReportSerializer(report).data
        if report.status == STATUS_PUBLIC or (report.status == STATUS_HIDE and code == code_true):
            if not code:
                addView(MODULE_REPORT, report.id)
            return Response(responseReport, status=status.HTTP_200_OK)
    return Response({'error': 'Отчет не найден'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_report_list_random(request, count):
    idUser = 0
    if request.user.is_authenticated:
        result = findUserLogin(request.user.username)
        if result['status'] == 'success' and result['user'].status == USER_STATUS_ACTIVE:
            idUser = result['user'].id

    reportList = readReportListRandom(count, idUser)
    responseReportList = ReportListSerializer(reportList, many=True).data
    return Response({'recCount': reportList.count(), 'reportList': responseReportList}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_report_like_toggle(request, pk):
    login = request.user.username
    loginStatus = checkUserStatus(login)
    if loginStatus['status'] == 'error':
        return Response(
            {'detail': loginStatus['message']},
            status=status.HTTP_401_UNAUTHORIZED
        )
    result = like_toggle(MODULE_REPORT, pk, loginStatus['user'].id)
    if result['status'] == 'success':
        return Response({'detail': result['message']}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': result['message']}, status=status.HTTP_400_BAD_REQUEST)

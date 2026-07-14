from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.constants import STATUS_PUBLIC, STATUS_HIDE
from core.libs import calcCodeTrue
from core.serializers import InfoListSerializer, InfoSerializer
from core.crud import readInfoList, readInfo, replaceTags


@api_view(['GET'])
def view_info_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 0))
    infoList = readInfoList()
    recCount = infoList.count()
    startRec = 0
    endRec = recCount
    if limit != 0 and recCount > limit:
        startRec = (page - 1) * limit
        endRec = page * limit
    responseInfoList = InfoListSerializer(infoList, many=True).data[startRec:endRec]
    return Response({'recCount': infoList.count(), 'infoList': responseInfoList}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_info(request, pk):
    info = readInfo(pk)
    code = request.GET.get('code', '')
    code_true = calcCodeTrue(pk, 0)
    if info:
        info.body = replaceTags(info.body)
        responseInfo = InfoSerializer(info).data
        if info.status == STATUS_PUBLIC or (info.status == STATUS_HIDE and code == code_true):
            return Response(responseInfo, status=status.HTTP_200_OK)
    return Response({'error': 'Сообщение не найдено'}, status=status.HTTP_404_NOT_FOUND)

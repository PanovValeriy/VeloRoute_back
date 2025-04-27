from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.crud import readNewsList

# Create your views here.

@api_view(['GET'])
def view_news_list(request):
  count = int(request.GET.get('count', 5))
  operation = int(request.GET.get('operation', 0))
  showEventArchive = request.GET.get('showEventArchive', 'false') == 'true'
  newsList = readNewsList(count, operation, showEventArchive)
  recCount = len(newsList)
  return Response({'recCount': recCount, 'newsList': newsList}, status=status.HTTP_200_OK)


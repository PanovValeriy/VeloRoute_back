from django.urls import path
from news.views import view_news_list

urlpatterns = [
    path('', view_news_list, name='eventList'),
]
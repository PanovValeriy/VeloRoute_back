from django.urls import path
from event.views import view_event_list, view_event, view_event_first

urlpatterns = [
    path('', view_event_list, name='eventList'),
    path('<int:pk>/', view_event, name='event'),
    path('first/', view_event_first, name='eventListFirst'),
]
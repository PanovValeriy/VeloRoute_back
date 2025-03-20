from django.urls import path
from event.views import view_event_list, view_event

urlpatterns = [
    path('', view_event_list, name='eventList'),
    path('<int:pk>/', view_event, name='event'),
]
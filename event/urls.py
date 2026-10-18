from django.urls import path
from event.views import view_event_list, view_event, view_event_first, view_event_member_toggle, view_event_like_toggle

urlpatterns = [
    path('', view_event_list, name='eventList'),
    path('<int:pk>/', view_event, name='event'),
    path('first/', view_event_first, name='eventListFirst'),
    path('member/<int:pk>/', view_event_member_toggle, name='memberToggle'),
    path('like/<int:pk>/', view_event_like_toggle, name='likeToggle'),
]
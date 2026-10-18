from django.urls import path
from route.views import view_route_list, view_route, view_route_list_random, view_route_like_toggle

urlpatterns = [
    path('', view_route_list, name='routeList'),
    path('<int:pk>/', view_route, name='route'),
    path('random/<int:count>/', view_route_list_random, name='routeListRandom'),
    path('like/<int:pk>/', view_route_like_toggle, name='routeLikeToggle'),
]
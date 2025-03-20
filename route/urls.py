from django.urls import path

from route.views import view_route_list, view_route

urlpatterns = [
    path('', view_route_list, name='routeList'),
    path('<int:pk>/', view_route, name='route'),
]
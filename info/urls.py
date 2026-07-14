from django.urls import path

from info.views import view_info_list, view_info

urlpatterns = [
    path('', view_info_list, name='infoList'),
    path('<int:pk>/', view_info, name='info'),
]
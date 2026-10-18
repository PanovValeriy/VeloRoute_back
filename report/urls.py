from django.urls import path

from report.views import view_report_list, view_report, view_report_list_random, view_report_like_toggle

urlpatterns = [
    path('', view_report_list, name='reportList'),
    path('<int:pk>/', view_report, name='report'),
    path('random/<int:count>/', view_report_list_random, name='reportListRandom'),
    path('like/<int:pk>/', view_report_like_toggle, name='reportLikeToggle'),
]
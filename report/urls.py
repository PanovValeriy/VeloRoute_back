from django.urls import path

from report.views import view_report_list, view_report

urlpatterns = [
    path('', view_report_list, name='reportList'),
    path('<int:pk>/', view_report, name='report'),
]
from django.contrib import admin
from django.urls import path, re_path, include
import core.views

urlpatterns = [
    path('', core.views.index),
    path('api/route/', include('route.urls')),
    path('api/report/', include('report.urls')),
    path('api/event/', include('event.urls')),
    path('admin/', admin.site.urls),
    re_path(r'[.]*', core.views.index)
]

from django.urls import path
from user.views import view_register, view_login, view_logout, view_profile, view_register_cancel

urlpatterns = [
    path('register/', view_register, name='register'),
    path('register/cancel/', view_register_cancel, name='registerCancel'),
    path('login/', view_login, name='login'),
    path('logout/', view_logout, name='logout'),
    path('profile/', view_profile, name='profile'),
]
# spotify/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('top_combined/', views.top_combined, name='top_combined'),
]

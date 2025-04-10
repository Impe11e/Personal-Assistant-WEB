from django.urls import path
from . import views

app_name = 'pers_assist_app'

urlpatterns = [
    path('', views.main, name='main'),
]

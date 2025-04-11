from django.urls import path
from . import views

app_name = 'pers_assist_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('contact_create/', views.contact_create, name='contact_create'),
    path('contact/<int:contact_id>/detail', views.contact_detail, name='contact_detail'),
    path('contact/<int:contact_id>/delete', views.contact_delete, name='contact_delete'),
]

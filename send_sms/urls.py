from django.urls import path
from . import views

app_name = 'send_sms'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'send/', views.send, name='send'),
    
]
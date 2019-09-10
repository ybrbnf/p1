from django.urls import path
from . import views

app_name = 'send_mail'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'send/', views.success, name='success'),
    

]

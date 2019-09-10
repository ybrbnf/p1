from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'add/', views.add, name='add'),
    path(r'consuming/', views.consuming, name='consuming'),
    path(r'upd/', views.consuming_upd, name='upd'),

]
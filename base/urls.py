from django.urls import path
from . import views

urlpatterns =[
    path('', views.lobby),
    path('room/<str:room_name>/',views.room,name='room'),

    path('get_token/',views.getToken),

    path('create_member/',views.createMember),
    path('get_member/',views.getMember),
    path('delete_member/',views.deleteMember),



]
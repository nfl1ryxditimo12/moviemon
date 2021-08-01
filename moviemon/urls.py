from django.urls import path

from .views import Title, Worldmap, finish, battle

urlpatterns = [
    path('', Title.as_view(), name='title'),
    path('worldmap/', Worldmap.as_view(), name='worldmap'),
    path('finish/', finish, name='finish'),
    path('batte/', battle, name='battle'),
]
from django.urls import path

from .views import Title, Worldmap, Battle, Moviedex, Detail, Option, Save, Load

urlpatterns = [
    path('', Title.as_view(), name='title'),
    path('worldmap/', Worldmap.as_view(), name='worldmap'),
    path('batte/<str:moviemon_id>', Battle.as_view(), name='battle'),
    path('moviedex/', Moviedex.as_view(), name='moviedex'),
    path('moviedex/<str:moviemon_id>', Detail.as_view(), name='detail'),
    path('options/', Option.as_view(), name='options'),
    path('options/save_game', Save.as_view(), name='save'),
    path('options/load_game', Load.as_view(), name='load'),
]
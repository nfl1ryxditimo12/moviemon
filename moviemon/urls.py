from django.urls import path

from .views import Title
from .views.worldmap import worldmap

urlpatterns = [
    path('title/', Title.as_view(), name='title'),
    path('worldmap/', worldmap, name='worldmap')
]
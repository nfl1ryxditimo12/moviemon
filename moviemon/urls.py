from django.urls import path

from . import views

urlpatterns = [
    path('title/', views.title, name='title')
]

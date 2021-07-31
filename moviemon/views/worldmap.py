from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class Worldmap(TemplateView):
    template_name = 'worldmap.html'
    
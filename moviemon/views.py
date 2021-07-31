from django.shortcuts import render

# Create your views here.

def title(request):
    return render(request, 'title.html')

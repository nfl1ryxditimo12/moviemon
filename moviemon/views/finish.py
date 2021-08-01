from django.shortcuts import render

def finish(request):
    return render(request, 'finish.html')
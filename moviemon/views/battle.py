from django.shortcuts import render, redirect

def battle(request):
    key = request.GET.get('key', None)
    if key == 'b':
        return redirect('worldmap')
    return render(request, 'battle.html')
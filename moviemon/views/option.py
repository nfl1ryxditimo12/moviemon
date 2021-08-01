from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class Option(TemplateView):
    template_name = 'option.html'
    
    def get(self, request):
        key = request.GET.get('key', None)

        if key == 'a':
            return redirect('save')
        elif key == 'b':
            return redirect('title')
        elif key == 'start':
            return redirect('worldmap')
        
        return render(request, self.template_name)
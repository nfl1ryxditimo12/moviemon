from moviemon.util.data import save_game_data, load_game_data, load_slot

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

state = {
    'slot': 0,
    'isLoad': False}

class Load(TemplateView):
    template_name = 'load.html'
    context = {}

    def get(self, request):

        key = request.GET.get('key', None)

        if (key is not None):
        
            if (key == 'up'):
                state['isLoad'] = False
                state['slot'] -= 1 if state['slot'] > 0 else 0
            elif (key == 'down'):
                state['isLoad'] = False
                state['slot'] += 1 if state['slot'] < 2 else 0
            if (key == 'a'):
                if state['isLoad'] == True:
                    state['isLoad'] = False
                    return redirect('worldmap')
                elif load_slot(('A', 'B', 'C')[state['slot']]):
                    state['isLoad'] = True
            elif (key == 'b'):
                return redirect('title')

            return redirect(request.path)

        slots = load_game_data()

        score = 'Free' if slots.get(
            'A', None) is None else slots.get('A').get('score', 'Free')
        self.context['A'] = "Slot 🅰 : {}".format(score)
        score = 'Free' if slots.get(
            'B', None) is None else slots.get('B').get('score', 'Free')
        self.context['B'] = "Slot 🅱 : {}".format(score)
        score = 'Free' if slots.get(
            'C', None) is None else slots.get('C').get('score', 'Free')
        self.context['C'] = "Slot 🅲 : {}".format(score)
        self.context['active'] = state['slot']
        self.context['btnA'] = 'Load'
        
        if state['isLoad'] == True:
            self.context['btnA'] = 'Start game'

        return render(request, self.template_name, self.context)
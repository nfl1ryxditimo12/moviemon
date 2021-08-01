from moviemon.util.data import GameData, load_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

state = {'idx': 0}

class Moviedex(TemplateView):
    template_name = 'moviedex.html'
    context = {}

    def get(self, request):
        game = GameData.load(load_session_data())
        key = request.GET.get('key', None)
        print(state['idx'])
        if key == 'right':
            if state['idx'] < len(game.captured_list) - 1:
                state['idx'] += 1
        elif key == 'left':
            if state['idx'] > 0:
                state['idx'] -= 1
        elif key == 'a':
            return redirect('detail', moviemon_id=game.captured_list[state['idx']])
        elif key == 'select':
            return redirect('worldmap')
        
        self.context['movies'] = []
        if state['idx'] > 0:
            id = game.captured_list[state['idx'] - 1]
            self.context['movies'].append({
                'poster': game.moviemon[id].poster,
                'class': 'moviedex-blur'
            })
        if len(game.captured_list) > 0:
            id = game.captured_list[state['idx']]
            self.context['movies'].append({
                'poster': game.moviemon[id].poster,
                'class': 'moviedex-ative '
            })
        if state['idx'] < len(game.captured_list) - 1:
            id = game.captured_list[state['idx'] + 1]
            self.context['movies'].append({
                'poster': game.moviemon[id].poster,
                'class': 'moviedex-blur'
            })
        if state['idx'] == 0 and 2 < len(game.captured_list):
            id = game.captured_list[2]
            self.context['movies'].append({
                'poster': game.moviemon[id].poster,
                'class': 'moviedex-blur'
            })
        return render(request, self.template_name, self.context)
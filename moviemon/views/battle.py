import random
from moviemon.util.data import GameData, load_session_data, save_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

state = {
    'id': "",
    'text': "",
    "button-text": "🅰 Throw the Ball   🅱 Leave",
    }

class Battle(TemplateView):
    template_name = 'battle.html'
    context = {}

    def calculate_percent(self, game, moviemon_id) -> int:
        percent = 50 - game.moviemon[moviemon_id].rating * 10 + game.get_strength() * 5
        if percent < 0:
            percent = 1
        elif percent >= 90:
            percent = 90
        return int(percent)

    def get(self, request, moviemon_id, key=None):
        game = GameData.load(load_session_data())

        key = request.GET.get('key', None)
        
        if moviemon_id not in game.captured_list:
            if moviemon_id != state['id']:
                state['text'] = " __{}__ is appeared !!".format(game.moviemon[moviemon_id].title)
                state['button-text'] = "🅰 Throw the Ball   🅱 Leave"
                state['id'] = moviemon_id

        if key is not None:
            if key == 'a':
                if moviemon_id not in game.captured_list:
                    if game.ball_count < 1:
                        state['text'] = "You have no Ball . . ."
                        state["button-text"] = "🅱 Continue"
                        return redirect(request.path)
                    game.ball_count -= 1
                    if random.randint(1, 101) <= self.calculate_percent(game, moviemon_id):
                        state['text'] = "Gotcha !!"
                        state["button-text"] = "🅱 Continue"
                        game.captured_list.append(moviemon_id)
                    else:
                        state['text'] = "Oh, you missed it !"
                save_session_data(game.dump())
            elif key == 'b':
                state["button-text"] = "🅱 Continue"
                save_session_data(game.dump())
                return redirect('worldmap')
            return redirect(request.path)

        self.context = {
            'title': game.moviemon[moviemon_id].title,
            'poster': game.moviemon[moviemon_id].poster,
            'rating': int(game.moviemon[moviemon_id].rating),
            'power': game.get_strength(),
            'ball': game.ball_count,
            'text': state['text'],
            'percent': self.calculate_percent(game, moviemon_id),
            'button_text': state['button-text']
        }
        return render(request, self.template_name, self.context)
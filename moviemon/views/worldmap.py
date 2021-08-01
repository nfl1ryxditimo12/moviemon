from rush00.settings import MOVIE_LIST
from moviemon.util.data import GameData, get_init_map, load_session_data, save_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

state = {'state': None}

class Worldmap(TemplateView):
    template_name = 'worldmap.html'
    context = {}

    def check_state(self, game: GameData):
        if len(game.captured_list) >= len(game.moviemon):
            print("Congraturation! You Win!")
            state['state'] = 'win'
        elif state['state'] == 'win':
            state['state'] = None

    def get(self, request):
        game = GameData.load(load_session_data())
        print(game.ball_count)
        print(game.map)
        key = request.GET.get('key', None)
        gotcha = "{now_count}/{total_count}".format(now_count=len(game.captured_list), total_count=len(game.moviemon.keys()))
        print(gotcha)
        print(state['state'])
        self.check_state(game)

        before_pos = {'x': game.pos['x'], 'y': game.pos['y']}

        if key and not state['state'] == 'win':
            if not state['state']:
                if key == 'up':
                    game.pos['x'] -= 1
                    if game.pos['x'] <= 0:
                        game.pos['x'] = 0
                elif key == 'down':
                    game.pos['x'] += 1
                    if game.pos['x'] >= 10:
                        game.pos['x'] = 9
                elif key == 'left':
                    game.pos['y'] -= 1
                    if game.pos['y'] <= 0:
                        game.pos['y'] = 0
                elif key == 'right':
                    game.pos['y'] += 1
                    if game.pos['y'] >= 10:
                        game.pos['y'] = 9
                elif key == 'start':
                    return redirect('options')
                elif key == 'select':
                    return redirect('moviedex')
            else:
                if key == 'a':
                    if state['state'] == 'battle':
                        state['state'] = None
                        return redirect('battle', moviemon_id=game.get_random_movie())

            if game.map[int(game.pos['x'])][int(game.pos['y'])] == 'ball':
                game.ball_count += 1
                game.map[int(game.pos['x'])][int(game.pos['y'])] = 'player'
                game.map[int(before_pos['x'])][int(before_pos['y'])] = 'ground'
            elif game.map[int(game.pos['x'])][int(game.pos['y'])] == 'ground':
                game.map[int(game.pos['x'])][int(game.pos['y'])] = 'player'
                game.map[int(before_pos['x'])][int(before_pos['y'])] = 'ground'
            elif game.map[int(game.pos['x'])][int(game.pos['y'])] == 'player':
                pass
            else:
                game.map[int(game.pos['x'])][int(game.pos['y'])] = 'player'
                game.map[int(before_pos['x'])][int(before_pos['y'])] = 'ground'
                state['state'] = 'battle'

            monster = 0
            for i in range(10):
                for j in range(10):
                    if game.map[i][j] in list(game.moviemon.keys()):
                        monster += 1
            if monster == 0:
                game.map = get_init_map(list(game.moviemon.keys()), game)

            save_session_data(game.dump())
            return redirect(request.path)
        elif key and key == 'a' and state['state'] == 'win':
            return redirect('title')

        self.context = {
            'state': state['state'],
            'game': game,
            'map': game.map
        }
        return render(request, self.template_name, self.context)
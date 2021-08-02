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
        # 맵, 좌표, 무비몬 리스트 등등 게임 데이터를 담는 인스턴스 변수
        game = GameData.load(load_session_data())
        key = request.GET.get('key', None)

        # 현재 잡은 무비몬의 갯수를 알려주는 변수
        gotcha = "{now_count}/{total_count}".format(now_count=len(game.captured_list), total_count=len(game.moviemon.keys()))
        print(gotcha)

        # 게임의 진행도를 전역변수를 통해 알려주는 함수
        self.check_state(game)

        # 키 입력 전 좌표를 저장하는 변수
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
            # state['state'] == 'battle' 인 경우
            else:
                if key == 'a':
                    if state['state'] == 'battle':
                        state['state'] = None
                        return redirect('battle', moviemon_id=game.get_random_movie())

            # 맵을 담는 리스트는 여기서 변경해준다
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

            # 만약 맵에 무비몬이 더이상 남아있지 않는 경우 맵을 새로 불러온다
            monster = 0
            for i in range(10):
                for j in range(10):
                    if game.map[i][j] in list(game.moviemon.keys()):
                        monster += 1
            if monster == 0:
                game.map = get_init_map(list(game.moviemon.keys()), game)

            # 세션 데이터 저장
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
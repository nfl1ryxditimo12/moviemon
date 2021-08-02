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

    # 무비몬 잡을 확률을 알려주는 함수
    def calculate_percent(self, game, moviemon_id) -> int:
        # 50 - 무비몬 평점 * 10 + 플레이어 힘 * 5
        percent = 50 - game.moviemon[moviemon_id].rating * 10 + game.get_strength() * 5
        if percent < 0:
            percent = 1
        elif percent >= 90:
            percent = 90
        return int(percent)

    def get(self, request, moviemon_id, key=None):

        # 게임 데이터를 불러온다
        game = GameData.load(load_session_data())

        key = request.GET.get('key', None)
        
        # Battle에서 출력할 텍스트의 기본값
        if moviemon_id not in game.captured_list:
            if moviemon_id != state['id']:
                state['text'] = "A wild Moviemon is appeared !!".format(game.moviemon[moviemon_id].title)
                state['button-text'] = "🅰 Throw the Ball   🅱 Leave"
                state['id'] = moviemon_id

        if key is not None:
            if key == 'a':
                if moviemon_id not in game.captured_list:

                    # 만약 소지한 Ball의 갯수가 0 일 경우 무한 리다이렉트
                    if game.ball_count < 1:
                        state['text'] = "You have no Ball . . ."
                        state["button-text"] = "🅱 Continue"
                        return redirect(request.path)

                    game.ball_count -= 1
                    
                    # 1 - 100 사이의 랜덤 수를 뽑아서 무비몬 잡을 확률 보다 낮으면 성공
                    # ex) 무비몬 잡을 확률 : 30%, 랜덤 수(1 - 100) : 25 -> 성공
                    if random.randint(1, 101) <= self.calculate_percent(game, moviemon_id):
                        state['text'] = "Gotcha !!"
                        state["button-text"] = "🅱 Continue"
                        game.captured_list.append(moviemon_id)

                    # 무비몬 잡을 확률보다 높으면 실패
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

            # get_strength() 함수에서 플레이어의 강함을 리턴해준다
            # 무비몬 한마리 잡을 때 마다 0.5씩 공격력이 올라간다
            'power': game.get_strength(),
            
            'ball': game.ball_count,
            'text': state['text'],
            'percent': self.calculate_percent(game, moviemon_id),
            'button_text': state['button-text']
        }
        return render(request, self.template_name, self.context)
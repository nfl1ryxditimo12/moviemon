import random
from moviemon.util.data import GameData, load_session_data, save_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

state = {
    'id': "",
    'text': "",
    "button-text": "๐ฐ๏ธ Throw the Ball   ๐ฑ๏ธ Leave",
    }

class Battle(TemplateView):
    template_name = 'battle.html'
    context = {}

    # ๋ฌด๋น๋ชฌ ์ก์ ํ๋ฅ ์ ์๋ ค์ฃผ๋ ํจ์
    def calculate_percent(self, game, moviemon_id) -> int:
        # 50 - ๋ฌด๋น๋ชฌ ํ์  * 10 + ํ๋ ์ด์ด ํ * 5
        percent = 50 - game.moviemon[moviemon_id].rating * 10 + game.get_strength() * 5
        if percent < 1:
            percent = 1
        elif percent > 90:
            percent = 90
        return int(percent)

    def get(self, request, moviemon_id, key=None):

        # ๊ฒ์ ๋ฐ์ดํฐ๋ฅผ ๋ถ๋ฌ์จ๋ค
        game = GameData.load(load_session_data())
        key = request.GET.get('key', None)
        
        # Battle์์ ์ถ๋ ฅํ  ํ์คํธ์ ๊ธฐ๋ณธ๊ฐ
        if moviemon_id not in game.captured_list:
            if moviemon_id != state['id']:
                state['text'] = "A wild Moviemon is appeared !!".format(game.moviemon[moviemon_id].title)
                state['button-text'] = "๐ฐ๏ธ Throw the Ball   ๐ฑ๏ธ Leave"
                state['id'] = moviemon_id

        if key is not None:
            if key == 'a':
                if moviemon_id not in game.captured_list:

                    # ๋ง์ฝ ์์งํ Ball์ ๊ฐฏ์๊ฐ 0 ์ผ ๊ฒฝ์ฐ ๋ฌดํ ๋ฆฌ๋ค์ด๋ ํธ
                    if game.ball_count < 1:
                        state['text'] = "You have no Ball . . ."
                        state["button-text"] = "๐ฑ๏ธ Continue"
                        return redirect(request.path)

                    game.ball_count -= 1
                    
                    # 1 - 100 ์ฌ์ด์ ๋๋ค ์๋ฅผ ๋ฝ์์ ๋ฌด๋น๋ชฌ ์ก์ ํ๋ฅ  ๋ณด๋ค ๋ฎ์ผ๋ฉด ์ฑ๊ณต
                    # ex) ๋ฌด๋น๋ชฌ ์ก์ ํ๋ฅ  : 30%, ๋๋ค ์(1 - 100) : 25 -> ์ฑ๊ณต
                    if random.randint(1, 101) <= self.calculate_percent(game, moviemon_id):
                        state['text'] = "Gotcha !!"
                        state["button-text"] = "๐ฑ๏ธ Continue"
                        game.captured_list.append(moviemon_id)

                    # ๋ฌด๋น๋ชฌ ์ก์ ํ๋ฅ ๋ณด๋ค ๋์ผ๋ฉด ์คํจ
                    else:
                        state['text'] = "Oh, you missed it !"

                save_session_data(game.dump())
            
            elif key == 'b':
                state["button-text"] = "๐ฑ๏ธ Continue"
                save_session_data(game.dump())
                return redirect('worldmap')

            return redirect(request.path)

        self.context = {
            'title': game.moviemon[moviemon_id].title,
            'poster': game.moviemon[moviemon_id].poster,
            'rating': int(game.moviemon[moviemon_id].rating),

            # get_strength() ํจ์์์ ํ๋ ์ด์ด์ ๊ฐํจ์ ๋ฆฌํดํด์ค๋ค
            # ๋ฌด๋น๋ชฌ ํ๋ง๋ฆฌ ์ก์ ๋ ๋ง๋ค 0.5์ฉ ๊ณต๊ฒฉ๋ ฅ์ด ์ฌ๋ผ๊ฐ๋ค
            'power': int(game.get_strength()),

            'ball': game.ball_count,
            'text': state['text'],
            'percent': self.calculate_percent(game, moviemon_id),
            'button_text': state['button-text']
        }
        return render(request, self.template_name, self.context)
from moviemon.util.data import GameData, load_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class Detail(TemplateView):
    template_name = 'detail.html'
    context = {}

    def get(self, request, moviemon_id):
        game = GameData.load(load_session_data())
        key = request.GET.get('key', None)

        if key == 'b':
            return redirect('moviedex')
        
        self.context = {
            'title': game.moviemon[moviemon_id].title,
            'poster': game.moviemon[moviemon_id].poster,
            'director': game.moviemon[moviemon_id].director,
            'year': game.moviemon[moviemon_id].year,
            'rating': game.moviemon[moviemon_id].rating,
            'actors': game.moviemon[moviemon_id].actors,
            'plot': game.moviemon[moviemon_id].plot
        }

        return render(request, self.template_name, self.context)
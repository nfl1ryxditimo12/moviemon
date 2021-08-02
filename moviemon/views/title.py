from moviemon.util.data import GameData, save_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
<<<<<<< HEAD

=======
>>>>>>> ddc2b234174801aceff1e52853ad2f711490aeeb
from moviemon.util.data import save_session_data

class Title(TemplateView):
    template_name = 'title.html'
    context = {}

    def get(self, request):
        key = request.GET.get('key', None)

        if key:
            print(key)
            if key == 'a':
                save_session_data(GameData.load_default_settings().dump())
                return redirect('worldmap')
            elif key == 'b':
                return redirect('loadfile')
            return redirect(request.path)
        return render(request, self.template_name, self.context)

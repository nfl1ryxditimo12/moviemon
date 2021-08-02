from moviemon.util.data import GameData, save_session_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#<<<<<<< HEAD

#=======
#>>>>>>> ddc2b234174801aceff1e52853ad2f711490aeeb
from moviemon.util.data import save_session_data

class Title(TemplateView):
    template_name = 'title.html'
    context = {}

    def get(self, request):
        key = request.GET.get('key', None)

        if key:
            print(key)
            if key == 'a':
                
                # 세선 데이터 저장
                save_session_data(GameData.load_default_settings().dump())

                # 월드맵으로 이동
                return redirect('worldmap')

            elif key == 'b':
                return redirect('load')
            return redirect(request.path)
        return render(request, self.template_name, self.context)

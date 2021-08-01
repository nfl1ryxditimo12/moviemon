import pickle
from moviemon.util.data import Moviemon


f =  open('save_game/movie_list.bin', 'rb')
data = dict(pickle.load(f))
f.close()

f =  open('save_game/save_game.bin', 'rb')
data1 = pickle.load(f)
f.close()

for value in data.values():
    print(value.title)

cnt = 0
ball = 0
for i in data1['map']:
    for j in i:
        if j != 'ground' and j != 'ball':
            cnt += 1
        if j == 'ball':
            ball += 1

print(cnt, ball)
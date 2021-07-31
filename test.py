import requests

apikey = "cd3c87f1"
url = "https://www.omdbapi.com/?apikey={apikey}&i=tt3896198".format(apikey=apikey)
data = requests.get(url).json()
print(data['Title'])
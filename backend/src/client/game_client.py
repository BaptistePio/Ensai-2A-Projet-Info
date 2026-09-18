import requests
import requests

url_test = (
    "https://raw.githubusercontent.com/"
    "BaptistePio/Ensai-2A-Projet-Info/"
    "sarahpalenne-tp4/data/game.json"
)

def get_games(url):
    response = requests.get(url)

    response.raise_for_status()

    return response.json()

r = get_games(url_test)

print(r)

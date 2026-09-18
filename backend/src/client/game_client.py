import requests

def get_game():
    r = requests.get('https://github.com/BaptistePio/Ensai-2A-Projet-Info/tree/sarahpalenne-tp4/data/game.json')
    return r 

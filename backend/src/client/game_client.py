import requests
from game_mode.player import Player


def get_games(id_game, player1, player2, winner, description, timestamp, game_mode):
    url = "https://github.com/BaptistePio/Ensai-2A-Projet-Info/blob/sarahpalenne-tp4/data/game.json"
    payload = {
        "id": id_game,
        "players_list": [
            player1,
            player2
            ],
        "winner_name": winner ,
        "details": description,
        "duration_seconds": timestamp,
        "mode_type": game_mode
  }
    r = requests.get(
        url,
        json = playload
        )
    return r.json()


import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.team = dict['team']
        self.goals = dict['goals']
        self.assists = dict['assists']
    
    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:1} + {self.assists:1} = {self.goals + self.assists:1}"

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = self.fetch_players()

    def fetch_players(self):
        response = requests.get(self.url).json()
        players = []
        for player_dict in response:
            players.append(Player(player_dict))
        return players
    
    def __iter__(self):
        return iter(self.players)  

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        filtered_players = [player for player in self.reader if player.nationality == nationality]
        sorted_players = sorted(filtered_players, key=lambda p: p.goals + p.assists, reverse=True)
        return sorted_players
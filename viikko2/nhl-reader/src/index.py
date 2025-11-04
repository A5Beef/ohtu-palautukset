from player import Player
import requests

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    #print("JSON-muotoinen vastaus:")
    #print(response)

    players = []

    for player_dict in response:
        player = Player(player_dict)

        if player.nationality == "FIN":
            players.append(player)
    
    players.sort(key=lambda p: p.goals + p.assists, reverse=True)

    print("Players from FIN")
    print()

    for player in players:
        print(player)


if __name__ == "__main__":
    main()

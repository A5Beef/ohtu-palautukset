from player import Player, PlayerStats, PlayerReader

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationality = "FIN"
    players = stats.top_scorers_by_nationality(nationality)

    print("Players from ", nationality)
    print("")
    for player in players:
        print(player)



if __name__ == "__main__":
    main()

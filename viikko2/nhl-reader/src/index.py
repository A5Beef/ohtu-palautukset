from player import Player, PlayerStats, PlayerReader
from rich.text import Text
from rich.console import Console
from rich.table import Table

def main():
    inputprompt = Text("Season ")
    inputprompt.append("[2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26]", style="bold magenta")
    inputprompt.append(": ")
    console = Console()
    season = console.input(inputprompt)
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    print()

    nationalityprompt = Text("Nationality ")
    nationalityprompt.append("[USA/FIN/CAN/SWE/CZE/RUS/SLO/FR/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS]", style="bold magenta")
    nationalityprompt.append(": ")

    while True:
        nationality = console.input(nationalityprompt)
        if nationality == "":
            break
        players = stats.top_scorers_by_nationality(nationality)

        print("")

        table = Table(title=f"Season {season} Players from {nationality}")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("teams", style="magenta")
        table.add_column("goals", style="green")
        table.add_column("assists", style="green")
        table.add_column("points", style="bold yellow")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))
        console.print(table)

if __name__ == "__main__":
    main()
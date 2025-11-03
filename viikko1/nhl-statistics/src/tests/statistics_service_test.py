import unittest
from statistics_service import StatisticsService
from player import Player  

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_returns_player_when_found(self):
        player = self.stats.search("Kurri")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 37)
        self.assertEqual(player.assists, 53)

    def test_search_returns_none_when_not_found(self):
        self.assertIsNone(self.stats.search("Nonexistent"))

    def test_team_returns_all_players_in_team(self):
        edm_players = self.stats.team("EDM")
        names = {p.name for p in edm_players}
        self.assertEqual(names, {"Semenko", "Kurri", "Gretzky"})

    def test_team_returns_empty_list_for_unknown_team(self):
        self.assertEqual(self.stats.team("ZZZ"), [])

    def test_top_returns_top_n_players_ordered_by_points(self):
        top3 = self.stats.top(3)
        self.assertEqual(len(top3), 3)
        self.assertEqual([p.name for p in top3],
                         ["Gretzky", "Lemieux", "Yzerman"])

    def test_top_handles_n_greater_than_player_count_and_zero(self):
        all_players = self.stats.top(100)
        self.assertEqual(len(all_players), 5)

        none_players = self.stats.top(0)
        self.assertEqual(none_players, [])

if __name__ == "__main__":
    unittest.main()


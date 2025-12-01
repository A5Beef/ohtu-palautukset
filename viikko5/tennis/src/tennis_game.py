class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def even_points(self):
        return self.m_score1 == self.m_score2
    def even_points_score(self):
        score = ""
        if self.m_score1 == 0:
            score = "Love-All"
        elif self.m_score1 == 1:
            score = "Fifteen-All"
        elif self.m_score1 == 2:
            score = "Thirty-All"
        else:
            score = "Deuce"
        return score
    def advantage_player(self):
        return self.m_score1 >= 4 or self.m_score2 >= 4
    def advantage_difference(self):
        minus_result = self.m_score1 - self. m_score2

        if minus_result == 1:
            score = "Advantage player1"
        elif minus_result == -1:
            score = "Advantage player2"

        elif minus_result >= 2:
            score = "Win for player1"
        else:
            score = "Win for player2"

        return score
    def score_counter(self):
        temp_score = 0
        score = ""
        for i in range(1, 3):
            if i == 1:
                temp_score = self.m_score1
            else:
                score = score + "-"
                temp_score = self.m_score2
            if temp_score == 0:
                score = score + "Love"
            elif temp_score == 1:
                score = score + "Fifteen"
            elif temp_score == 2:
                score = score + "Thirty"
            elif temp_score == 3:
                score = score + "Forty"
        return score
    def get_score(self):
        if self.even_points():
            return self.even_points_score()
        if self.advantage_player():
            return self.advantage_difference()
        return self.score_counter()

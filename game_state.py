import time

class GameState:
    def __init__(self, player):
        self.player = player
        self.last_rep_time = 0

    def can_rep(self):
        return time.time() - self.last_rep_time >= self.player.get_current_rest_time()

    def perform_rep(self):
        if not self.can_rep():
            return "⏳ Resting..."

        self.last_rep_time = time.time()
        self.player.reps += 1
        earned = self.player.earn_bucks()
        self.player.strength_bucks += earned

        return f"🏋️‍♂️ Rep done! Earned ${earned}."
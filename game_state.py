import time

class GameState:
    def __init__(self, player):
        self.player = player
        self.last_rep_time = 0

    def can_rep(self):
        return time.time() - self.last_rep_time >= self.player.base_rest_time

    def time_until_next_rep(self):
        return max(0, int(self.player.base_rest_time - (time.time() - self.last_rep_time)))

    def perform_rep(self):
        if not self.can_rep():
            return f"⏳ Recovering... {self.time_until_next_rep()}s left"
        self.last_rep_time = time.time()
        self.player.reps += 1
        earned = self.player.weight // 5
        self.player.strength_bucks += earned
        return f"✅ Rep completed with {self.player.weight} lbs! +${earned}"

    def display_rest_time(self):
        return f"Cooldown: {self.player.base_rest_time:.1f}s"

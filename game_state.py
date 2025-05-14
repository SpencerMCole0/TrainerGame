import time

class GameState:
    def __init__(self, player):
        self.player = player
        self.fatigue = 0
        self.rep_count = 0
        self.resting_until = 0  # timestamp in seconds

    def is_resting(self):
        return time.time() < self.resting_until

    def time_remaining(self):
        remaining = self.resting_until - time.time()
        return max(0, int(remaining))

    def perform_rep(self):
        if self.is_resting():
            return f"⏳ Resting... {self.time_remaining()}s left"
        if self.fatigue >= 5:
            return "😩 You're too fatigued. Rest first."
        self.rep_count += 1
        self.fatigue += 1
        earned = self.player.weight // 5
        self.player.strength_bucks += earned
        return f"✅ Rep completed! +${earned}"

    def rest(self, rest_seconds=5):
        self.resting_until = time.time() + rest_seconds
        if self.player.path == "weightlifting":
            self.player.reps += 1
        else:
            self.player.weight += 5
        self.fatigue = 0
        self.rep_count = 0
        return f"💤 Resting for {rest_seconds} seconds..."

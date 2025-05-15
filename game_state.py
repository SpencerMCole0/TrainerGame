import time

class GameState:
    def __init__(self, player):
        self.player = player
        self.last_rep_time = 0

    def can_rep(self):
        return time.time() - self.last_rep_time >= self.player.base_rest_time

    def time_until_next_rep(self):
        remaining = self.player.base_rest_time - (time.time() - self.last_rep_time)
        return max(0, round(remaining, 1))

    def calculate_rest_time(self, weight):
        if weight <= 135:
            return 1.0 + (weight - 45) / 90 * 4.0  # Linear scaling from 1s (45 lbs) to 5s (135 lbs)
        else:
            return 5.0 + (0.5 * (weight - 135)**0.5)  # Logarithmic-like growth

    def perform_rep(self):
        if not self.can_rep():
            return "⏳ Still resting..."

        earned = self.player.weight // 5 + self.player.extra_bucks_per_rep
        self.player.strength_bucks += earned
        self.player.reps += 1

        # Scale rest time with barbell weight
        base = self.calculate_rest_time(self.player.barbell_weight)
        recovery = self.player.recovery_bonus
        self.player.base_rest_time = max(1.0, base - recovery)

        self.last_rep_time = time.time()
        return f"✅ Rep done! Earned ${earned}."

class GameState:
    def __init__(self, player):
        self.player = player
        self.fatigue = 0
        self.rep_count = 0

    def perform_rep(self):
        if self.fatigue >= 5:
            return "Too tired! Rest first."
        self.rep_count += 1
        self.fatigue += 1
        earned = self.player.weight // 5
        self.player.strength_bucks += earned
        return f"Rep completed! +${earned}"

    def rest(self):
        if self.player.path == "weightlifting":
            self.player.reps += 1
        else:
            self.player.weight += 5
        self.fatigue = 0
        self.rep_count = 0
        return "Rested. Stats improved!"

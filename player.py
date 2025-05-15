class Player:
    def __init__(self, path):
        self.path = path
        self.strength_bucks = 0
        self.reps = 0
        self.total_weight = 135  # total owned
        self.barbell_weight = 135  # current selected weight
        self.base_rest_time = 5.0
        self.min_rest_time = 1.0
        self.extra_bucks_per_rep = 0
        self.upgrades = []

    def reduce_rest_time(self, amount):
        self.base_rest_time = max(self.min_rest_time, self.base_rest_time - amount)

    def add_weight(self):
        self.total_weight += 5
        self.base_rest_time += 0.5

    def use_steroids(self):
        self.base_rest_time = max(self.min_rest_time, self.base_rest_time - 1.0)

    def increase_barbell(self):
        if self.barbell_weight + 5 <= self.total_weight:
            self.barbell_weight += 5
            return "⬆️ Increased barbell weight."
        return "❌ You don't own enough weight."

    def decrease_barbell(self):
        if self.barbell_weight - 5 >= 45:  # Min barbell weight
            self.barbell_weight -= 5
            return "⬇️ Decreased barbell weight."
        return "❌ Barbell can't go lower."

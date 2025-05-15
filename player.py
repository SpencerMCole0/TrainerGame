class Player:
    def __init__(self, path):
        self.path = path
        self.reps = 0
        self.strength_bucks = 0
        self.total_weight = 135
        self.barbell_weight = 135
        self.extra_bucks_per_rep = 0
        self.base_weight = 135
        self.min_rest_time = 1.0
        self.rest_reduction = 0.0
        self.recovery_items_purchased = {}

    def add_weight(self, amount=5):
        self.total_weight += amount
        self.barbell_weight += amount

    def get_current_rest_time(self):
        base_time = 5.0 * (self.barbell_weight / self.base_weight)
        return max(self.min_rest_time, base_time - self.rest_reduction)

    def add_income_boost(self, amount):
        self.extra_bucks_per_rep += amount

    def reduce_rest_time(self, amount):
        self.rest_reduction += amount

    def earn_bucks(self):
        return (self.barbell_weight // 5) + self.extra_bucks_per_rep

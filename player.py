class Player:
    def __init__(self, path):
        self.path = path
        self.strength_bucks = 0
        self.reps = 0
        self.weight = 135
        self.base_rest_time = 5.0
        self.min_rest_time = 1.0
        self.upgrades = []

    def add_weight(self):
        self.weight += 5
        self.base_rest_time += 0.5

    def use_steroids(self):
        self.base_rest_time = max(self.min_rest_time, self.base_rest_time - 1.0)

class Player:
    def __init__(self, path):
        self.path = path
        self.strength_bucks = 0
        self.reps = 1
        self.weight = 5
        self.max_reps = 5
        self.max_weight = 50
        self.upgrades = []

    def add_bucks(self, amount):
        self.strength_bucks += amount

    def apply_upgrade(self, upgrade):
        self.upgrades.append(upgrade)
        upgrade.apply(self)

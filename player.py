import json
import os

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

    def to_dict(self):
            return {
                "path": self.path,
                "reps": self.reps,
                "strength_bucks": self.strength_bucks,
                "total_weight": self.total_weight,
                "barbell_weight": self.barbell_weight,
                "extra_bucks_per_rep": self.extra_bucks_per_rep,
            }

    def from_dict(self, data):
        self.path = data.get("path", self.path)
        self.reps = data.get("reps", self.reps)
        self.strength_bucks = data.get("strength_bucks", self.strength_bucks)
        self.total_weight = data.get("total_weight", self.total_weight)
        self.barbell_weight = data.get("barbell_weight", self.barbell_weight)
        self.extra_bucks_per_rep = data.get("extra_bucks_per_rep", self.extra_bucks_per_rep)

    def save(self, filename="savegame.json"):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    def load(self, filename="savegame.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.from_dict(data)
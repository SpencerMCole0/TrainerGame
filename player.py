import json
import os

class Player:
    def reset(self):
        self.path = "No Path"
        self.reps = 0
        self.strength_bucks = 0
        self.total_weight = 135
        self.barbell_weight = 135
        self.extra_bucks_per_rep = 0

    def __init__(self, path):
        self.path = path
        self.reps = 0
        self.strength_bucks = 0
        self.base_bar_weight = 20.0  # Olympic bar weight in kg
        self.plates = {
            0.5: 0,
            1: 0,
            2: 0,
            2.5: 0,
            5: 0,
            10: 0,
            15: 0,
            20: 0,
            25: 0
        }
        self.recovery_rest_time_values = {
            "r1": 0.2,
            "r2": 0.4,
            "r3": 0.6,
            "r4": 0.8,
            "r5": 1.0,
            "r6": 1.2,
            "r7": 1.4,
            "r8": 1.6,
            "r9": 1.8,
            "r10": 2.0,
        }
        self.purchased_recovery_items = {
            "r1": 0,
            "r2": 0,
            "r3": 0,
            "r4": 0,
            "r5": 0,
            "r6": 0,
            "r7": 0,
            "r8": 0,
            "r9": 0,
            "r10": 0,
        }
        self.barbell_weight = self.base_bar_weight  # Start with just the bar
        self.extra_bucks_per_rep = 0
        self.min_rest_time = 1.0
        self.rest_reduction = 0.0
        self.bucks_per_rep = 0
        self.recovery_items_purchased = {}
        self.purchased_sponsorship_items = {
            "s1": 0,
            "s2": 0,
            "s3": 0,
            "s4": 0,
            "s5": 0,
            "s6": 0,
            "s7": 0,
            "s8": 0,
            "s9": 0,
            "s10": 0,
        }

        # Sponsorship bonus dictionary (bucks per rep)
        self.sponsorships = {
            "s1": {"bonus": 5},
            "s2": {"bonus": 10},
            "s3": {"bonus": 15},
            "s4": {"bonus": 20},
            "s5": {"bonus": 25},
            "s6": {"bonus": 30},
            "s7": {"bonus": 35},
            "s8": {"bonus": 40},
            "s9": {"bonus": 45},
            "s10": {"bonus": 50},
        }

    def add_weight(self, amount=5):
        self.total_weight += amount
        self.barbell_weight += amount

    def get_total_rest_time_reduction(self):
        # Sum all recovery items' rest time reductions
        # For example, you might store these in a dict or have a list of purchased items
        # Here is a simple placeholder that sums all recovery rest time reductions:

        total_reduction = 0.0
        for item_id, quantity in self.purchased_recovery_items.items():
            rest_time_reduction = self.get_recovery_item_rest_time(item_id)  # Define this method to get reduction per item_id
            total_reduction += rest_time_reduction * quantity
        return total_reduction

    def get_current_rest_time(self):
        # Convert barbell_weight from lbs to kg for calculation
        barbell_kg = self.barbell_weight * 0.453592
        base_kg = 60.0  # base kg weight for 5 seconds cooldown
        base_time = 5.0 * (barbell_kg / base_kg)
        reduced_time = base_time - self.get_total_rest_time_reduction()
        min_time = 1.0
        return max(reduced_time, min_time)

    def add_income_boost(self, amount):
        self.extra_bucks_per_rep += amount

    def get_total_rest_time_reduction(self):
            total_reduction = 0.0
            for item_id, qty in self.purchased_recovery_items.items():
                total_reduction += self.recovery_rest_time_values.get(item_id, 0) * qty
            return total_reduction

    def add_recovery_item(self, item_id):
        if item_id in self.purchased_recovery_items:
            self.purchased_recovery_items[item_id] += 1

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

    def calculate_total_weight(self):
        plate_total = 0
        for weight, count in self.plates.items():
            plate_total += weight * count * 2  # plates on both sides
        self.barbell_weight = self.base_bar_weight + plate_total
        return self.barbell_weight

    def add_plate(self, weight):
        if weight in self.plates:
            self.plates[weight] += 1
            self.calculate_total_weight()
    
    def remove_plate(self, weight):
        if weight in self.plates and self.plates[weight] > 0:
            self.plates[weight] -= 1
            self.calculate_total_weight()

    def get_sponsorship_bonus(self):
        # Sum bucks per rep bonus from all purchased sponsorship items
        total_bonus = 0
        for key, count in self.purchased_sponsorship_items.items():
            if key in self.sponsorships:
                bonus = self.sponsorships[key]['bonus']
                total_bonus += bonus * count
        return total_bonus

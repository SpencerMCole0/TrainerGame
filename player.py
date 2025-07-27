import json
import os
import math
import time

class Player:
    def __init__(self, path=None):
        self.path = path
        self.reset()

    def reset(self):
        self.path = None
        self.reps = 0
        self.strength_bucks = 0

        self.base_bar_weight = 20.0  # Olympic barbell
        self.plates = {
            0.5: 0, 1: 0, 2: 0, 2.5: 0,
            5: 0, 10: 0, 15: 0, 20: 0, 25: 0
        }

        # Simplified cooldown system
        self.base_rest_time = 3.0
        self.min_rest_time = 0.5

        self.barbell_weight = self.base_bar_weight
        self.bucks_per_rep = 0

        # Recovery Upgrades
        self.recovery_rest_time_values = {
            "r1": 0.2, "r2": 0.4, "r3": 0.6, "r4": 0.8, "r5": 1.0,
            "r6": 1.2, "r7": 1.4, "r8": 1.6, "r9": 1.8, "r10": 2.0
        }
        self.purchased_recovery_items = {key: 0 for key in self.recovery_rest_time_values}

        # Sponsorship Bonuses
        self.purchased_sponsorship_items = {f"s{i}": 0 for i in range(1, 11)}
        self.sponsorships = {
            f"s{i}": {"bonus": i * 5} for i in range(1, 11)
        }

        self.last_rep_timestamp = time.time()

    @property
    def total_weight(self):
        plates_weight = sum(weight * count * 2 for weight, count in self.plates.items())
        return self.base_bar_weight + plates_weight

    def calculate_total_weight(self):
        self.barbell_weight = self.total_weight

    def add_plate(self, weight):
        if weight in self.plates:
            self.plates[weight] += 1
            self.calculate_total_weight()

    def remove_weight(self, weight):
        if weight in self.plates and self.plates[weight] > 0:
            self.plates[weight] -= 1
            self.calculate_total_weight()

    def get_total_rest_time_reduction(self):
        return sum(
            self.recovery_rest_time_values.get(item_id, 0) * count
            for item_id, count in self.purchased_recovery_items.items()
        )

    def get_current_rest_time(self):
        return max(self.base_rest_time - self.get_total_rest_time_reduction(), self.min_rest_time)

    def get_sponsorship_bonus(self):
        return sum(
            self.sponsorships.get(item_id, {}).get("bonus", 0) * count
            for item_id, count in self.purchased_sponsorship_items.items()
        )

    def earn_bucks(self):
        base = 10
        bonus = self.bucks_per_rep + self.get_sponsorship_bonus()
        total = base + bonus
        self.strength_bucks += total
        self.last_rep_timestamp = time.time()
        return total

    def get_bucks_per_second(self):
        cooldown = self.get_current_rest_time()
        earnings = 10 + self.bucks_per_rep + self.get_sponsorship_bonus()
        return round(earnings / cooldown, 2)

    def add_income_boost(self, amount):
        self.bucks_per_rep += amount

    def reduce_rest_time(self, amount):
        for item_id, val in self.recovery_rest_time_values.items():
            if val == amount:
                self.purchased_recovery_items[item_id] += 1
                break

    # === Save/Load ===
    def save(self, filename):
        data = {
            'reps': self.reps,
            'strength_bucks': self.strength_bucks,
            'plates': self.plates,
            'purchased_recovery_items': self.purchased_recovery_items,
            'purchased_sponsorship_items': self.purchased_sponsorship_items,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        self.path = filename

    def load(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No save file found: {filename}")
        with open(filename, 'r') as f:
            data = json.load(f)

        self.reset()
        self.reps = data.get('reps', 0)
        self.strength_bucks = data.get('strength_bucks', 0)
        self.plates = {float(k): v for k, v in data.get('plates', {}).items()}
        self.calculate_total_weight()
        self.purchased_recovery_items = data.get('purchased_recovery_items', {})
        self.purchased_sponsorship_items = data.get('purchased_sponsorship_items', {})
        self.path = filename

    def get_cooldown_debug_info(self):
        return {
            "Cooldown Time": round(self.get_current_rest_time(), 2),
            "Reps": self.reps,
            "Rest Reduction": round(self.get_total_rest_time_reduction(), 2),
            "Min Rest Cap Hit": self.get_current_rest_time() == self.min_rest_time,
            "Bucks/Rep": 10 + self.bucks_per_rep + self.get_sponsorship_bonus(),
            "Bucks/Sec": self.get_bucks_per_second(),
        }

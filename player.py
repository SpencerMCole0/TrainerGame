import json
import os
import math

class Player:
    def __init__(self, path=None):
        self.path = path
        self.reset()

    def reset(self):
        self.path = None
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
            25: 0,
        }

        # Cooldown mechanics
        self.base_rest_time = 3.0     # NEW: baseline cooldown in seconds
        self.min_rest_time = 0.5      # NEW: absolute cooldown floor
        self.rest_reduction = 0.0     # legacy value; no longer used directly

        self.barbell_weight = self.base_bar_weight
        self.bucks_per_rep = 0

        # Recovery system
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
        self.purchased_recovery_items = {key: 0 for key in self.recovery_rest_time_values}

        # Sponsorship system
        self.purchased_sponsorship_items = {f"s{i}": 0 for i in range(1, 11)}
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

    @property
    def total_weight(self):
        plates_weight = sum(weight * count * 2 for weight, count in self.plates.items())
        return self.base_bar_weight + plates_weight

    def add_weight(self, amount):
        if amount in self.plates:
            self.plates[amount] += 1
            self.calculate_total_weight()

    def remove_weight(self, amount):
        if amount in self.plates and self.plates[amount] > 0:
            self.plates[amount] -= 1
            self.calculate_total_weight()

    def calculate_total_weight(self):
        total_plates_weight = sum(weight * count * 2 for weight, count in self.plates.items())
        self.barbell_weight = self.base_bar_weight + total_plates_weight

    def get_total_rest_time_reduction(self):
        return sum(
            self.recovery_rest_time_values.get(item_id, 0) * count
            for item_id, count in self.purchased_recovery_items.items()
        )

    def get_current_rest_time(self):
        fatigue_multiplier = (self.barbell_weight / self.base_bar_weight) * math.log(self.reps + 1)
        raw_cooldown = self.base_rest_time * fatigue_multiplier
        final_cooldown = max(raw_cooldown - self.get_total_rest_time_reduction(), self.min_rest_time)
        return final_cooldown

    def get_sponsorship_bonus(self):
        return sum(
            self.sponsorships.get(item_id, {}).get('bonus', 0) * count
            for item_id, count in self.purchased_sponsorship_items.items()
        )

    def earn_bucks(self):
        base_earnings = 10
        total_earnings = base_earnings + self.bucks_per_rep + self.get_sponsorship_bonus()
        self.strength_bucks += total_earnings
        return total_earnings

    def add_income_boost(self, amount):
        self.bucks_per_rep += amount

    def reduce_rest_time(self, amount):
        # Find which recovery item this amount corresponds to
        for item_id, val in self.recovery_rest_time_values.items():
            if val == amount:
                self.purchased_recovery_items[item_id] += 1
                break

    def add_plate(self, weight):
        if weight in self.plates:
            self.plates[weight] += 1
            self.calculate_total_weight()

    # === Save and Load Methods ===
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
        fatigue_multiplier = (self.barbell_weight / self.base_bar_weight) * math.log(self.reps + 1)
        raw_cooldown = self.base_rest_time * fatigue_multiplier
        rest_reduction = self.get_total_rest_time_reduction()
        final_cooldown = max(raw_cooldown - rest_reduction, self.min_rest_time)

        return {
            "Cooldown Time": round(final_cooldown, 2),
            "Fatigue Multiplier": round(fatigue_multiplier, 2),
            "Reps": self.reps,
            "Base Rest Time": self.base_rest_time,
            "Rest Reduction": round(rest_reduction, 2),
            "Min Rest Cap Hit": final_cooldown == self.min_rest_time
        }

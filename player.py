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
        self.gym_coins = 0.0

        self.base_bar_weight = 20.0  # Olympic barbell
        self.plates = {
            0.5: 0, 1: 0, 2: 0, 2.5: 0,
            5: 0, 10: 0, 15: 0, 20: 0, 25: 0
        }

        # Click economy
        self.rep_value_base = 0.1  # base GymCoins per rep
        self.prestige_level = 0

        # Simplified cooldown system
        self.base_rest_time = 3.0
        self.min_rest_time = 0.5

        self.barbell_weight = self.base_bar_weight

        # Career multipliers (click, passive)
        self.career_multipliers = {
            "Weightlifting": (1.0, 1.0),
            "Powerlifting": (1.3, 0.8),
            "Bodybuilding": (0.85, 1.25),
            "Crossfit": (1.05, 1.05),
        }

        # Idle trainers (passive reps/sec)
        self.trainer_level = 0
        self.trainer_base_rate = 0.02  # reps per second per trainer

        # Active session budget (two 10-minute sessions per day at ~2 reps/sec)
        self.daily_active_budget = 2 * 10 * 60  # seconds
        self.active_seconds_remaining = self.daily_active_budget
        self.daily_sessions_used = 0
        self.current_session_seconds_remaining = 0.0
        self._active_day = time.localtime().tm_yday

        # Recovery Upgrades (reduces rest time)
        self.recovery_rest_time_values = {
            "r1": 0.2, "r2": 0.4, "r3": 0.6, "r4": 0.8, "r5": 1.0,
            "r6": 1.2, "r7": 1.4, "r8": 1.6, "r9": 1.8, "r10": 2.0
        }
        self.purchased_recovery_items = {key: 0 for key in self.recovery_rest_time_values}

        # Sponsorship multipliers (permanent percent multipliers to GymCoins)
        self.purchased_sponsorship_items = {f"s{i}": 0 for i in range(1, 11)}
        self.sponsorships = {
            f"s{i}": {"mult": 0.05 * i} for i in range(1, 11)
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

    def get_career_multipliers(self):
        # Returns (click_mult, passive_mult)
        return self.career_multipliers.get(self.path, (1.0, 1.0))

    def get_equipment_multiplier(self):
        # More weight gives more GymCoins per rep (diminishing returns)
        extra_weight = max(0.0, self.total_weight - self.base_bar_weight)
        return extra_weight / 100.0  # 0.01 per kg above base

    def get_recovery_multiplier(self):
        # Rest reduction provides a small bonus
        return min(0.5, self.get_total_rest_time_reduction() / 10.0)

    def get_sponsorship_multiplier(self):
        return sum(
            self.sponsorships.get(item_id, {}).get("mult", 0) * count
            for item_id, count in self.purchased_sponsorship_items.items()
        )

    def get_prestige_factor(self):
        # Each Legend Point gives +2% to base value (multiplicative)
        return 1.02 ** self.prestige_level

    def get_total_multiplier(self):
        # The sum of all non-career multipliers (as a percent bonus)
        return (
            self.get_equipment_multiplier()
            + self.get_recovery_multiplier()
            + self.get_sponsorship_multiplier()
        )

    def get_gymcoins_per_rep(self):
        base = self.rep_value_base
        click_mult, _ = self.get_career_multipliers()
        mult = 1 + self.get_total_multiplier()
        return base * click_mult * mult * self.get_prestige_factor()

    def earn_gym_coins(self, reps=1):
        earned = reps * self.get_gymcoins_per_rep()
        self.gym_coins += earned
        self.last_rep_timestamp = time.time()
        return earned

    def get_passive_reps_per_second(self):
        # Trainers generate passive reps over time
        _, passive_mult = self.get_career_multipliers()
        base_rate = self.trainer_base_rate * self.trainer_level
        return base_rate * passive_mult

    def get_passive_gymcoins_per_second(self):
        # Passive income converts reps to GymCoins using the same multipliers
        # but using the passive career multiplier.
        base = self.rep_value_base
        _, passive_mult = self.get_career_multipliers()
        mult = 1 + self.get_total_multiplier()
        return base * passive_mult * mult * self.get_prestige_factor() * self.trainer_level * self.trainer_base_rate

    def get_gymcoins_per_second(self):
        # Active clicking rate (based on cooldown and rep value)
        cooldown = self.get_current_rest_time()
        return round(self.get_gymcoins_per_rep() / cooldown, 2)

    def prestige(self):
        """Reset progression for a permanent prestige bonus."""
        self.prestige_level += 1
        self.reps = 0
        self.gym_coins = 0.0
        self.trainer_level = 0
        self.plates = {w: 0 for w in self.plates}
        self.purchased_recovery_items = {k: 0 for k in self.purchased_recovery_items}
        self.purchased_sponsorship_items = {k: 0 for k in self.purchased_sponsorship_items}
        self.calculate_total_weight()

    def add_trainer(self):
        self.trainer_level += 1

    def add_sponsorship_multiplier(self, amount):
        # amount is a decimal fraction (e.g., 0.05 for +5%)
        # Find a sponsorship entry with a matching multiplier (if any)
        for item_id, info in self.sponsorships.items():
            if abs(info.get("mult", 0) - amount) < 1e-9:
                self.purchased_sponsorship_items[item_id] += 1
                return
        # If no existing sponsorship entry matches, add as a custom multiplier
        key = f"custom_{amount}"
        self.purchased_sponsorship_items[key] = self.purchased_sponsorship_items.get(key, 0) + 1
        self.sponsorships[key] = {"mult": amount}

    # Legacy compatibility
    def add_income_boost(self, amount):
        # Convert an income boost (legacy dollars-per-rep) into a percent multiplier
        # (Assumes base rep value of 0.1 GymCoins)
        # Example: $10 per rep => 10 / (0.1) = 100x, but we scale it down.
        self.add_sponsorship_multiplier(amount * 0.001)

    def reduce_rest_time(self, amount):
        for item_id, val in self.recovery_rest_time_values.items():
            if val == amount:
                self.purchased_recovery_items[item_id] += 1
                break

    # === Save/Load ===
    def save(self, filename):
        data = {
            'reps': self.reps,
            'gym_coins': self.gym_coins,
            'plates': self.plates,
            'purchased_recovery_items': self.purchased_recovery_items,
            'purchased_sponsorship_items': self.purchased_sponsorship_items,
            'prestige_level': self.prestige_level,
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
        # Backwards compatibility: allow old saves with strength_bucks
        self.gym_coins = data.get('gym_coins', data.get('strength_bucks', 0))
        self.plates = {float(k): v for k, v in data.get('plates', {}).items()}
        self.calculate_total_weight()
        self.purchased_recovery_items = data.get('purchased_recovery_items', {})
        self.purchased_sponsorship_items = data.get('purchased_sponsorship_items', {})
        self.prestige_level = data.get('prestige_level', 0)
        self.path = filename

    def get_cooldown_debug_info(self):
        return {
            "Cooldown Time": round(self.get_current_rest_time(), 2),
            "Active Remaining": round(max(0.0, self.active_seconds_remaining), 1),
            "Session Remaining": round(max(0.0, self.current_session_seconds_remaining), 1),
            "Sessions Used": self.daily_sessions_used,
            "Reps": self.reps,
            "Rest Reduction": round(self.get_total_rest_time_reduction(), 2),
            "Min Rest Cap Hit": self.get_current_rest_time() == self.min_rest_time,
            "GymCoins/Rep": round(self.get_gymcoins_per_rep(), 2),
            "GymCoins/Sec": self.get_gymcoins_per_second(),
        }

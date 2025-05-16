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

        self.barbell_weight = self.base_bar_weight

        self.bucks = 0
        self.bucks_per_rep = 0

        self.min_rest_time = 1.0
        self.rest_reduction = 0.0

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
        # total plates weight on both sides + bar weight
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
        total_reduction = 0.0
        for item_id, count in self.purchased_recovery_items.items():
            total_reduction += self.recovery_rest_time_values.get(item_id, 0) * count
        return total_reduction

    def get_current_rest_time(self):
        base_time = 5.0 * (self.barbell_weight / self.base_bar_weight)
        reduced_time = base_time - self.get_total_rest_time_reduction()
        return max(reduced_time, self.min_rest_time)

    def get_sponsorship_bonus(self):
        total_bonus = 0
        for item_id, count in self.purchased_sponsorship_items.items():
            total_bonus += self.sponsorships.get(item_id, {}).get('bonus', 0) * count
        return total_bonus
    
    def earn_bucks(self):
        base_earnings = 10  # or whatever base bucks per rep you want
        total_earnings = base_earnings + self.bucks_per_rep + self.get_sponsorship_bonus()
        self.strength_bucks += total_earnings
        return total_earnings  # Return amount earned for display if needed


class StoreItem:
    def __init__(self, name, cost, description, action, limit=None):
        self.name = name
        self.cost = cost
        self.description = description
        self.action = action
        self.limit = limit
        self.times_bought = 0

    def can_buy(self, player):
        if player.strength_bucks < self.cost:
            return (False, "Not enough bucks!")
        if self.limit is not None and self.times_bought >= self.limit:
            return (False, "Max purchases reached!")
        return (True, "")

    def buy(self, player):
        can_buy, msg = self.can_buy(player)
        if not can_buy:
            return f"❌ {msg}"

        player.strength_bucks -= self.cost
        self.action(player)
        self.times_bought += 1
        return f"✅ Purchased {self.name}!"

    def get_effect(self):
        return self.description


class Store:
    def __init__(self):
        self.items = {
            # Recovery Items
            "r1": StoreItem("-0.2s rest time", 50, "-0.2s rest time", lambda p: p.reduce_rest_time(0.2), 200),
            "r2": StoreItem("-0.4s rest time", 100, "-0.4s rest time", lambda p: p.reduce_rest_time(0.4), 180),
            "r3": StoreItem("-0.6s rest time", 150, "-0.6s rest time", lambda p: p.reduce_rest_time(0.6), 160),
            "r4": StoreItem("-0.8s rest time", 200, "-0.8s rest time", lambda p: p.reduce_rest_time(0.8), 140),
            "r5": StoreItem("-1.0s rest time", 250, "-1.0s rest time", lambda p: p.reduce_rest_time(1.0), 120),
            "r6": StoreItem("-1.2s rest time", 300, "-1.2s rest time", lambda p: p.reduce_rest_time(1.2), 100),
            "r7": StoreItem("-1.4s rest time", 350, "-1.4s rest time", lambda p: p.reduce_rest_time(1.4), 80),
            "r8": StoreItem("-1.6s rest time", 400, "-1.6s rest time", lambda p: p.reduce_rest_time(1.6), 60),
            "r9": StoreItem("-1.8s rest time", 450, "-1.8s rest time", lambda p: p.reduce_rest_time(1.8), 40),
            "r10": StoreItem("-2.0s rest time", 500, "-2.0s rest time", lambda p: p.reduce_rest_time(2.0), 20),

            # Sponsorships
            "s1": StoreItem("+$5 bucks per rep", 50, "Earn +$5 bucks per rep", lambda p: p.add_income_boost(5), 200),
            "s2": StoreItem("+$10 bucks per rep", 100, "Earn +$10 bucks per rep", lambda p: p.add_income_boost(10), 180),
            "s3": StoreItem("+$15 bucks per rep", 150, "Earn +$15 bucks per rep", lambda p: p.add_income_boost(15), 160),
            "s4": StoreItem("+$20 bucks per rep", 200, "Earn +$20 bucks per rep", lambda p: p.add_income_boost(20), 140),
            "s5": StoreItem("+$25 bucks per rep", 250, "Earn +$25 bucks per rep", lambda p: p.add_income_boost(25), 120),
            "s6": StoreItem("+$30 bucks per rep", 300, "Earn +$30 bucks per rep", lambda p: p.add_income_boost(30), 100),
            "s7": StoreItem("+$35 bucks per rep", 350, "Earn +$35 bucks per rep", lambda p: p.add_income_boost(35), 80),
            "s8": StoreItem("+$40 bucks per rep", 400, "Earn +$40 bucks per rep", lambda p: p.add_income_boost(40), 60),
            "s9": StoreItem("+$45 bucks per rep", 450, "Earn +$45 bucks per rep", lambda p: p.add_income_boost(45), 40),
            "s10": StoreItem("+$50 bucks per rep", 500, "Earn +$50 bucks per rep", lambda p: p.add_income_boost(50), 20),

            # Weights
            "w1": StoreItem("Add Weight", 100, "Add +5 lbs to barbell (slower reps)", lambda p: p.add_weight()),
        }

    def get_items(self):
        return self.items

    def get_grouped_items(self):
        return (
            [key for key in self.items if key.startswith("r")],
            [key for key in self.items if key.startswith("s")],
            [key for key in self.items if key.startswith("w")],
        )

class StoreItem:
    def __init__(self, name, cost, description, action, limit=None):
        self.name = name
        self.cost = cost
        self.description = description
        self.action = action
        self.limit = limit
        self.times_bought = 0

    def can_buy(self, player):
        if self.limit is not None and self.times_bought >= self.limit:
            return False, "🔒 Limit reached for this item."
        if player.strength_bucks < self.cost:
            return False, "💸 Not enough bucks!"
        return True, ""

    def buy(self, player):
        can_buy, msg = self.can_buy(player)
        if not can_buy:
            return msg
        player.strength_bucks -= self.cost
        self.times_bought += 1
        return self.action(player)


class Store:
    def __init__(self):
        self.recovery_items = {
            "recovery1": StoreItem("Recovery #1", 50, "-0.2s rest time", lambda p: p.reduce_rest_time(0.2)),
            "recovery2": StoreItem("Recovery #2", 100, "-0.4s rest time", lambda p: p.reduce_rest_time(0.4)),
            "recovery3": StoreItem("Recovery #3", 150, "-0.6s rest time", lambda p: p.reduce_rest_time(0.6)),
            "recovery4": StoreItem("Recovery #4", 200, "-0.8s rest time", lambda p: p.reduce_rest_time(0.8)),
            "recovery5": StoreItem("Recovery #5", 250, "-1.0s rest time", lambda p: p.reduce_rest_time(1.0)),
            "recovery6": StoreItem("Recovery #6", 300, "-1.2s rest time", lambda p: p.reduce_rest_time(1.2)),
            "recovery7": StoreItem("Recovery #7", 350, "-1.4s rest time", lambda p: p.reduce_rest_time(1.4)),
            "recovery8": StoreItem("Recovery #8", 400, "-1.6s rest time", lambda p: p.reduce_rest_time(1.6)),
            "recovery9": StoreItem("Recovery #9", 450, "-1.8s rest time", lambda p: p.reduce_rest_time(1.8)),
            "recovery10": StoreItem("Recovery #10", 500, "-2.0s rest time", lambda p: p.reduce_rest_time(2.0)),
        }


        self.sponsorship_items = {
            "placeholder1": StoreItem("Placeholder #1", 50, "Earn +$5 bucks per rep", lambda p: p.add_income_boost(5)),
            "placeholder2": StoreItem("Placeholder #2", 100, "Earn +$10 bucks per rep", lambda p: p.add_income_boost(10)),
            "placeholder3": StoreItem("Placeholder #3", 150, "Earn +$15 bucks per rep", lambda p: p.add_income_boost(15)),
            "placeholder4": StoreItem("Placeholder #4", 200, "Earn +$20 bucks per rep", lambda p: p.add_income_boost(20)),
            "placeholder5": StoreItem("Placeholder #5", 250, "Earn +$25 bucks per rep", lambda p: p.add_income_boost(25)),
            "placeholder6": StoreItem("Placeholder #6", 300, "Earn +$30 bucks per rep", lambda p: p.add_income_boost(30)),
            "placeholder7": StoreItem("Placeholder #7", 350, "Earn +$35 bucks per rep", lambda p: p.add_income_boost(35)),
            "placeholder8": StoreItem("Placeholder #8", 400, "Earn +$40 bucks per rep", lambda p: p.add_income_boost(40)),
            "placeholder9": StoreItem("Placeholder #9", 450, "Earn +$45 bucks per rep", lambda p: p.add_income_boost(45)),
            "placeholder10": StoreItem("Placeholder #10", 500, "Earn +$50 bucks per rep", lambda p: p.add_income_boost(50)),
        }


        self.weight_items = {
            "weight": StoreItem("Add Weight", 100, "Add +5 lbs to barbell (slower reps)", lambda p: p.add_weight())
        }

    def get_grouped_items(self):
        return [
            list(self.recovery_items.keys()),
            list(self.sponsorship_items.keys()),
            list(self.weight_items.keys())
        ]

    def get_items(self):
        return {**self.recovery_items, **self.sponsorship_items, **self.weight_items}

    def purchase(self, key, player):
        all_items = self.get_items()
        if key in all_items:
            return all_items[key].buy(player)
        return "❌ Item not found!"

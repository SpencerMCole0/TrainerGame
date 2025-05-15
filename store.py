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
            "protein": StoreItem("Protein Shake", 50, "-0.25s rest time (Max 5)", lambda p: p.reduce_rest_time(0.25), limit=5),
            "icebath": StoreItem("Ice Bath", 100, "-0.5s rest time (Max 3)", lambda p: p.reduce_rest_time(0.5), limit=3),
            "massage": StoreItem("Massage", 200, "-1.0s rest time", lambda p: p.reduce_rest_time(1.0)),
            "sauna": StoreItem("Sauna", 400, "-1.5s rest time", lambda p: p.reduce_rest_time(1.5)),
            "steroids": StoreItem("Use Steroids", 250, "Reduce rest time by 1s (min 1s)", lambda p: p.use_steroids())
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

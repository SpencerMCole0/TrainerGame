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
            return False, "🔒 Limit reached for this recovery method."
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
        recovery_items = {
            "protein": StoreItem(
                name="Protein Shake",
                cost=50,
                description="-0.25s rest time (Max 5)",
                action=lambda p: p.reduce_rest_time(0.25),
                limit=5
            ),
            "icebath": StoreItem(
                name="Ice Bath",
                cost=100,
                description="-0.5s rest time (Max 3)",
                action=lambda p: p.reduce_rest_time(0.5),
                limit=3
            ),
            "massage": StoreItem(
                name="Massage",
                cost=200,
                description="-1.0s rest time",
                action=lambda p: p.reduce_rest_time(1.0)
            ),
            "sauna": StoreItem(
                name="Sauna",
                cost=400,
                description="-1.5s rest time",
                action=lambda p: p.reduce_rest_time(1.5)
            )
        }

        training_items = {
            "weight": StoreItem(
                name="Add Weight",
                cost=100,
                description="Add +5 lbs to barbell (slower reps)",
                action=lambda p: p.add_weight()
            ),
            "steroids": StoreItem(
                name="Use Steroids",
                cost=250,
                description="Reduce rest time by 1s (min 1s)",
                action=lambda p: p.use_steroids()
            ),
            "accessory": StoreItem(
                name="Accessory Work",
                cost=150,
                description="Earn +1 buck per rep",
                action=lambda p: p.add_income_boost(1)
            ),
            "competition": StoreItem(
                name="Competition",
                cost=300,
                description="Earn +2 bucks per rep",
                action=lambda p: p.add_income_boost(2)
            ),
            "sponsor": StoreItem(
                name="Sponsorship Deal",
                cost=500,
                description="Earn +5 bucks per rep",
                action=lambda p: p.add_income_boost(5)
            )
        }

        self.items = {**recovery_items, **training_items}
        self.recovery_keys = list(recovery_items.keys())
        self.training_keys = list(training_items.keys())

    def get_items(self):
        return self.items

    def get_grouped_items(self):
        return self.recovery_keys, self.training_keys

    def purchase(self, key, player):
        item = self.items.get(key)
        if not item:
            return "❌ Invalid item."
        return item.buy(player)

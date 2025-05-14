class StoreItem:
    def __init__(self, name, cost, description, action):
        self.name = name
        self.cost = cost
        self.description = description
        self.action = action  # function(player) -> str (feedback message)

class Store:
    def __init__(self):
        self.items = {
            "weight": StoreItem(
                name="Add Weight",
                cost=100,
                description="Add +5 lbs to barbell (slower reps)",
                action=self.add_weight
            ),
            "steroids": StoreItem(
                name="Use Steroids",
                cost=250,
                description="Reduce rest time by 1s (min 1s)",
                action=self.use_steroids
            )
        }

    def get_items(self):
        return self.items

    def purchase(self, key, player):
        item = self.items.get(key)
        if not item:
            return "❌ Invalid item."
        if player.strength_bucks < item.cost:
            return "💸 Not enough bucks!"
        player.strength_bucks -= item.cost
        return item.action(player)

    def add_weight(self, player):
        player.add_weight()
        return "🏋️ Added 5 lbs to barbell!"

    def use_steroids(self, player):
        player.use_steroids()
        return "💉 Steroids used. Rest time reduced!"

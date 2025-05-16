class StoreItem:
    def __init__(self, name, cost, description, action, limit=None):
        self.name = name
        self.cost = cost
        self.description = description
        self.action = action  # function to apply effect to player
        self.limit = limit  # max purchase count
        self.times_bought = 0

    def can_buy(self, player):
        if self.limit is not None and self.times_bought >= self.limit:
            return (False, "Max limit reached")
        if player.strength_bucks < self.cost:
            return (False, "Not enough bucks")
        return (True, "")

    def buy(self, player):
        can_buy, msg = self.can_buy(player)
        if not can_buy:
            return f"❌ {msg}"
        player.strength_bucks -= self.cost
        self.times_bought += 1
        self.action(player)
        return f"✅ Purchased {self.name}!"



class Upgrade:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description
        self.is_purchased = False

    def purchase(self, player):
        if player.strength_bucks >= self.cost:
            player.strength_bucks -= self.cost
            self.is_purchased = True
            return f"Purchased {self.name}!"
        else:
            return "Not enough strength bucks."



class UpgradeStore:
    def __init__(self):
        self.upgrades = []

    def add_upgrade(self, upgrade):
        self.upgrades.append(upgrade)

    def purchase_upgrade(self, index, player):
        if 0 <= index < len(self.upgrades):
            return self.upgrades[index].purchase(player)
        return "Invalid upgrade index."

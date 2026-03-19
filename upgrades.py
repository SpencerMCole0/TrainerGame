class StoreItem:
    def __init__(self, name, base_cost, description, action, limit=None, growth=1.15):
        self.name = name
        self.base_cost = base_cost
        self.description = description
        self.action = action  # function to apply effect to player
        self.limit = limit  # max purchase count
        self.times_bought = 0
        self.growth = growth

    @property
    def cost(self):
        # Exponential cost scaling based on times bought
        return int(self.base_cost * (self.growth ** self.times_bought))

    def can_buy(self, player):
        if self.limit is not None and self.times_bought >= self.limit:
            return (False, "Max limit reached")
        if player.gym_coins < self.cost:
            return (False, "Not enough GymCoins")
        return (True, "")

    def buy(self, player):
        can_buy, msg = self.can_buy(player)
        if not can_buy:
            return f"❌ {msg}"
        player.gym_coins -= self.cost
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
        if player.gym_coins >= self.cost:
            player.gym_coins -= self.cost
            self.is_purchased = True
            return f"Purchased {self.name}!"
        else:
            return "Not enough GymCoins."



class UpgradeStore:
    def __init__(self):
        self.upgrades = []

    def add_upgrade(self, upgrade):
        self.upgrades.append(upgrade)

    def purchase_upgrade(self, index, player):
        if 0 <= index < len(self.upgrades):
            return self.upgrades[index].purchase(player)
        return "Invalid upgrade index."

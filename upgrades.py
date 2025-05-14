class Upgrade:
    def __init__(self, name, cost, apply_func):
        self.name = name
        self.cost = cost
        self.apply = apply_func

class UpgradeStore:
    def __init__(self):
        self.upgrades = {
            "protein": Upgrade("Protein Shake", 50, lambda p: setattr(p, 'reps', p.reps + 1)),
            "coach": Upgrade("Online Coach", 100, lambda p: setattr(p, 'weight', p.weight + 10)),
            "steroids": Upgrade("Steroids 💉", 500, lambda p: setattr(p, 'reps', p.reps + 5)),
        }

    def show_upgrades(self):
        print("\n🛒 Upgrade Store:")
        for key, up in self.upgrades.items():
            print(f"{key.title()}: {up.name} - ${up.cost}")
        print()

    def purchase(self, choice, player):
        upgrade = self.upgrades.get(choice.lower())
        if not upgrade:
            print("❌ Upgrade not found.")
            return
        if player.strength_bucks >= upgrade.cost:
            player.strength_bucks -= upgrade.cost
            player.apply_upgrade(upgrade)
            print(f"✅ Bought {upgrade.name}!")
        else:
            print("💸 Not enough Strength Bucks!")

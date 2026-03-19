from upgrades import StoreItem

store_items = {
    # Recovery items
    "r1": StoreItem("-0.2s rest time", 50, "Reduces rest time by 0.2 seconds", lambda p, amt=0.2: p.reduce_rest_time(amt), limit=200),
    "r2": StoreItem("-0.4s rest time", 100, "Reduces rest time by 0.4 seconds", lambda p, amt=0.4: p.reduce_rest_time(amt), limit=180),
    "r3": StoreItem("-0.6s rest time", 150, "Reduces rest time by 0.6 seconds", lambda p, amt=0.6: p.reduce_rest_time(amt), limit=160),
    "r4": StoreItem("-0.8s rest time", 200, "Reduces rest time by 0.8 seconds", lambda p, amt=0.8: p.reduce_rest_time(amt), limit=140),
    "r5": StoreItem("-1.0s rest time", 250, "Reduces rest time by 1.0 seconds", lambda p, amt=1.0: p.reduce_rest_time(amt), limit=120),
    "r6": StoreItem("-1.2s rest time", 300, "Reduces rest time by 1.2 seconds", lambda p, amt=1.2: p.reduce_rest_time(amt), limit=100),
    "r7": StoreItem("-1.4s rest time", 350, "Reduces rest time by 1.4 seconds", lambda p, amt=1.4: p.reduce_rest_time(amt), limit=80),
    "r8": StoreItem("-1.6s rest time", 400, "Reduces rest time by 1.6 seconds", lambda p, amt=1.6: p.reduce_rest_time(amt), limit=60),
    "r9": StoreItem("-1.8s rest time", 450, "Reduces rest time by 1.8 seconds", lambda p, amt=1.8: p.reduce_rest_time(amt), limit=40),
    "r10": StoreItem("-2.0s rest time", 500, "Reduces rest time by 2.0 seconds", lambda p, amt=2.0: p.reduce_rest_time(amt), limit=20),

    # Sponsorships: permanent GymCoin multipliers (percent)
    "s1": StoreItem("Local Sponsor", 100, "+5% GymCoins per rep", lambda p, amt=0.05: p.add_sponsorship_multiplier(amt), limit=50, growth=1.15),
    "s2": StoreItem("Regional Sponsor", 200, "+10% GymCoins per rep", lambda p, amt=0.10: p.add_sponsorship_multiplier(amt), limit=40, growth=1.15),
    "s3": StoreItem("National Sponsor", 400, "+15% GymCoins per rep", lambda p, amt=0.15: p.add_sponsorship_multiplier(amt), limit=30, growth=1.15),
    "s4": StoreItem("Brand Partnership", 800, "+20% GymCoins per rep", lambda p, amt=0.20: p.add_sponsorship_multiplier(amt), limit=20, growth=1.15),
    "s5": StoreItem("Mega Sponsor", 1600, "+25% GymCoins per rep", lambda p, amt=0.25: p.add_sponsorship_multiplier(amt), limit=15, growth=1.15),

    # Trainer hires (passive reps/sec)
    "t1": StoreItem("Hire Trainer", 50, "Adds a trainer that generates passive reps over time.", lambda p: p.add_trainer(), limit=None, growth=1.15),

    # Kilogram plates for barbell
    "p0_5": StoreItem("Buy 0.5kg Plate", 5, "Add one 0.5kg plate (each side)", lambda p, wt=0.5: p.add_plate(wt), limit=20),
    "p1": StoreItem("Buy 1kg Plate", 10, "Add one 1kg plate (each side)", lambda p, wt=1: p.add_plate(wt), limit=20),
    "p2": StoreItem("Buy 2kg Plate", 15, "Add one 2kg plate (each side)", lambda p, wt=2: p.add_plate(wt), limit=20),
    "p2_5": StoreItem("Buy 2.5kg Plate", 20, "Add one 2.5kg plate (each side)", lambda p, wt=2.5: p.add_plate(wt), limit=20),
    "p5": StoreItem("Buy 5kg Plate", 30, "Add one 5kg plate (each side)", lambda p, wt=5: p.add_plate(wt), limit=20),
    "p10": StoreItem("Buy 10kg Plate", 60, "Add one 10kg plate (each side)", lambda p, wt=10: p.add_plate(wt), limit=20),
    "p15": StoreItem("Buy 15kg Plate", 90, "Add one 15kg plate (each side)", lambda p, wt=15: p.add_plate(wt), limit=20),
    "p20": StoreItem("Buy 20kg Plate", 120, "Add one 20kg plate (each side)", lambda p, wt=20: p.add_plate(wt), limit=20),
    "p25": StoreItem("Buy 25kg Plate", 150, "Add one 25kg plate (each side)", lambda p, wt=25: p.add_plate(wt), limit=20),
}

class Store:
    def __init__(self):
        self.items = store_items

    def get_items(self):
        return self.items

    def get_grouped_items(self):
        recovery = [k for k in self.items if k.startswith("r")]
        sponsorship = [k for k in self.items if k.startswith("s")]
        trainers = [k for k in self.items if k.startswith("t")]
        weights = [k for k in self.items if k.startswith("p")]
        return recovery, sponsorship, trainers, weights

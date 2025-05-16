from upgrades import StoreItem

store_items = {
    # Recovery items
    "r1": StoreItem("-0.2s rest time", 50, "Reduces rest time by 0.2 seconds", lambda p: p.reduce_rest_time(0.2), limit=200),
    "r2": StoreItem("-0.4s rest time", 100, "Reduces rest time by 0.4 seconds", lambda p: p.reduce_rest_time(0.4), limit=180),
    "r3": StoreItem("-0.6s rest time", 150, "Reduces rest time by 0.6 seconds", lambda p: p.reduce_rest_time(0.6), limit=160),
    "r4": StoreItem("-0.8s rest time", 200, "Reduces rest time by 0.8 seconds", lambda p: p.reduce_rest_time(0.8), limit=140),
    "r5": StoreItem("-1.0s rest time", 250, "Reduces rest time by 1.0 seconds", lambda p: p.reduce_rest_time(1.0), limit=120),
    "r6": StoreItem("-1.2s rest time", 300, "Reduces rest time by 1.2 seconds", lambda p: p.reduce_rest_time(1.2), limit=100),
    "r7": StoreItem("-1.4s rest time", 350, "Reduces rest time by 1.4 seconds", lambda p: p.reduce_rest_time(1.4), limit=80),
    "r8": StoreItem("-1.6s rest time", 400, "Reduces rest time by 1.6 seconds", lambda p: p.reduce_rest_time(1.6), limit=60),
    "r9": StoreItem("-1.8s rest time", 450, "Reduces rest time by 1.8 seconds", lambda p: p.reduce_rest_time(1.8), limit=40),
    "r10": StoreItem("-2.0s rest time", 500, "Reduces rest time by 2.0 seconds", lambda p: p.reduce_rest_time(2.0), limit=20),

    # Sponsorship placeholders
    "s1": StoreItem("Placeholder #1", 50, "Adds $5 per rep", lambda p: p.add_income_boost(5), limit=200),
    "s2": StoreItem("Placeholder #2", 100, "Adds $10 per rep", lambda p: p.add_income_boost(10), limit=180),
    "s3": StoreItem("Placeholder #3", 150, "Adds $15 per rep", lambda p: p.add_income_boost(15), limit=160),
    "s4": StoreItem("Placeholder #4", 200, "Adds $20 per rep", lambda p: p.add_income_boost(20), limit=140),
    "s5": StoreItem("Placeholder #5", 250, "Adds $25 per rep", lambda p: p.add_income_boost(25), limit=120),
    "s6": StoreItem("Placeholder #6", 300, "Adds $30 per rep", lambda p: p.add_income_boost(30), limit=100),
    "s7": StoreItem("Placeholder #7", 350, "Adds $35 per rep", lambda p: p.add_income_boost(35), limit=80),
    "s8": StoreItem("Placeholder #8", 400, "Adds $40 per rep", lambda p: p.add_income_boost(40), limit=60),
    "s9": StoreItem("Placeholder #9", 450, "Adds $45 per rep", lambda p: p.add_income_boost(45), limit=40),
    "s10": StoreItem("Placeholder #10", 500, "Adds $50 per rep", lambda p: p.add_income_boost(50), limit=20),

    # Kilogram plates for barbell
    "p0_5": StoreItem("Buy 0.5kg Plate", 5, "Add one 0.5kg plate (each side)", lambda p: p.add_plate(0.5), limit=20),
    "p1": StoreItem("Buy 1kg Plate", 10, "Add one 1kg plate (each side)", lambda p: p.add_plate(1), limit=20),
    "p2": StoreItem("Buy 2kg Plate", 15, "Add one 2kg plate (each side)", lambda p: p.add_plate(2), limit=20),
    "p2_5": StoreItem("Buy 2.5kg Plate", 20, "Add one 2.5kg plate (each side)", lambda p: p.add_plate(2.5), limit=20),
    "p5": StoreItem("Buy 5kg Plate", 30, "Add one 5kg plate (each side)", lambda p: p.add_plate(5), limit=20),
    "p10": StoreItem("Buy 10kg Plate", 60, "Add one 10kg plate (each side)", lambda p: p.add_plate(10), limit=20),
    "p15": StoreItem("Buy 15kg Plate", 90, "Add one 15kg plate (each side)", lambda p: p.add_plate(15), limit=20),
    "p20": StoreItem("Buy 20kg Plate", 120, "Add one 20kg plate (each side)", lambda p: p.add_plate(20), limit=20),
    "p25": StoreItem("Buy 25kg Plate", 150, "Add one 25kg plate (each side)", lambda p: p.add_plate(25), limit=20),
}

class Store:
    def __init__(self):
        self.items = store_items

    def get_items(self):
        return self.items

    def get_grouped_items(self):
        recovery = [k for k in self.items if k.startswith("r")]
        sponsorship = [k for k in self.items if k.startswith("s")]
        weights = [k for k in self.items if k.startswith("p")]
        return recovery, sponsorship, weights

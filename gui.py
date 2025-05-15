import pygame
from store import Store

class Button:
    def __init__(self, text, x, y, w, h, callback, font, enabled=True, color=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.font = font
        self.enabled = enabled
        self.color = color if color else (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class GameGUI:
    def __init__(self, screen, player, game_state):
        self.screen = screen
        self.player = player
        self.game_state = game_state
        self.font = pygame.font.SysFont("arial", 24)
        self.message = ""
        self.in_store = False
        self.active_tab = "recovery"
        self.store = Store()

        self.buttons = []

        self.tab_buttons = [
            Button("🧃 Recovery", 50, 10, 150, 40, lambda: self.set_tab("recovery"), self.font),
            Button("🏋️ Training", 220, 10, 150, 40, lambda: self.set_tab("training"), self.font),
        ]

        self.page_buttons = []

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_game()

    def draw_game(self):
        self.buttons = []

        do_rep_btn = Button("Do Rep", 100, 450, 150, 50, self.do_rep, self.font)
        open_store_btn = Button("Open Store", 300, 450, 150, 50, self.toggle_store, self.font)

        # ✅ Fix: enforce minimum barbell weight of 45 lbs
        can_decrease = self.player.barbell_weight > 45
        can_increase = self.player.total_weight > self.player.barbell_weight

        dec_color = (200, 200, 200) if can_decrease else (100, 100, 100)
        inc_color = (200, 200, 200) if can_increase else (100, 100, 100)

        dec_btn = Button("- Weight", 100, 510, 150, 40, self.decrease_barbell, self.font, enabled=can_decrease, color=dec_color)
        inc_btn = Button("+ Weight", 300, 510, 150, 40, self.increase_barbell, self.font, enabled=can_increase, color=inc_color)

        self.buttons.extend([do_rep_btn, open_store_btn, dec_btn, inc_btn])

        for btn in self.buttons:
            btn.draw(self.screen)

        stats = [
            f"Path: {self.player.path.title()}",
            f"Reps: {self.player.reps}",
            f"Total Owned Weight: {self.player.total_weight} lbs",
            f"Barbell Weight: {self.player.barbell_weight} lbs",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {self.player.base_rest_time:.1f}s",
        ]

        if not self.game_state.can_rep():
            stats.append(f"⏳ Rest: {self.game_state.time_until_next_rep()}s remaining")

        stats.append(f"Message: {self.message}")

        for i, line in enumerate(stats):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (50, 50 + i * 30))

        self.draw_cooldown_bar()

    def draw_store(self):
        screen_width = self.screen.get_width()
        content_x = 50
        content_y = 60

        for tab in self.tab_buttons:
            if (tab.text == "🧃 Recovery" and self.active_tab == "recovery") or \
               (tab.text == "🏋️ Training" and self.active_tab == "training"):
                tab.color = (180, 255, 180)
            else:
                tab.color = (200, 200, 200)
            tab.draw(self.screen)

        title = self.font.render("🏪 Store", True, (255, 255, 0))
        self.screen.blit(title, (content_x, content_y))

        y = content_y + 50

        recovery_keys, training_keys = self.store.get_grouped_items()
        keys_to_render = recovery_keys if self.active_tab == "recovery" else training_keys

        for key in keys_to_render:
            item = self.store.items[key]
            self.screen.blit(self.font.render(f"{item.name} - ${item.cost}", True, (255, 255, 255)), (content_x, y))
            self.screen.blit(self.font.render(item.description, True, (180, 180, 180)), (content_x, y + 30))
            y += 70

        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (content_x, y))
        y += 40
        self.screen.blit(self.font.render(self.message, True, (255, 255, 255)), (content_x, y))

        y += 60
        self.page_buttons = []

        item_buttons = []
        for key in keys_to_render:
            item = self.store.items[key]

            def make_callback(k):
                return lambda: self.buy_item(k)

            can_afford, _ = item.can_buy(self.player)
            color = (200, 200, 200) if can_afford else (100, 100, 100)

            # ✅ Fix: widen button to prevent text overflow
            btn = Button(
                f"Buy {item.name} (${item.cost})",
                0, 0, 320, 50,
                make_callback(key),
                self.font,
                enabled=can_afford,
                color=color
            )
            item_buttons.append(btn)

        # Layout item buttons
        buttons_per_row = 3
        spacing = 20
        row_height = 50
        for i, btn in enumerate(item_buttons):
            row = i // buttons_per_row
            col = i % buttons_per_row
            row_items = item_buttons[row * buttons_per_row: (row + 1) * buttons_per_row]
            row_width = sum(b.rect.width for b in row_items) + spacing * (len(row_items) - 1)
            start_x = (screen_width - row_width) // 2
            x = start_x + col * (btn.rect.width + spacing)
            y_pos = y + row * (row_height + spacing)
            btn.rect.topleft = (x, y_pos)
            btn.draw(self.screen)

        self.page_buttons = item_buttons.copy()

        y += ((len(item_buttons) + buttons_per_row - 1) // buttons_per_row) * (row_height + spacing) + 10
        back_btn = Button("Back to Gym", (screen_width - 180) // 2, y, 180, 50, self.toggle_store, self.font, color=(255, 100, 100))
        back_btn.draw(self.screen)
        self.page_buttons.append(back_btn)

    def draw_cooldown_bar(self):
        if not self.game_state.can_rep():
            full_width = 600
            height = 20
            x = 100
            y = 400

            time_left = self.game_state.time_until_next_rep()
            total = self.player.base_rest_time
            fill_ratio = 1 - (time_left / total)

            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, full_width, height))
            pygame.draw.rect(self.screen, (0, 200, 0), (x, y, int(full_width * fill_ratio), height))

    def handle_event(self, event):
        if self.in_store:
            for btn in self.tab_buttons + self.page_buttons:
                btn.handle_event(event)
        else:
            for btn in self.buttons:
                btn.handle_event(event)

    def toggle_store(self):
        self.in_store = not self.in_store
        self.message = ""

    def set_tab(self, tab_name):
        self.active_tab = tab_name

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def buy_item(self, key):
        self.message = self.store.purchase(key, self.player)

    def buy_weight(self):
        self.message = self.store.purchase("weight", self.player)

    def buy_steroids(self):
        self.message = self.store.purchase("steroids", self.player)

    def increase_barbell(self):
        self.message = self.player.increase_barbell()

    def decrease_barbell(self):
        self.message = self.player.decrease_barbell()

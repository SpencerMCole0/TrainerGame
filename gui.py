import pygame
from store import Store

class Button:
    def __init__(self, text, x, y, w, h, callback, font):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.font = font
        self.color = (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class GameGUI:
    def __init__(self, screen, player, game_state):
        self.screen = screen
        self.player = player
        self.game_state = game_state
        self.font = pygame.font.SysFont("arial", 24)
        self.message = ""
        self.in_store = False
        self.store = Store()

        self.buttons = [
            Button("Do Rep", 100, 450, 150, 50, self.do_rep, self.font),
            Button("Open Store", 300, 450, 150, 50, self.toggle_store, self.font),
        ]

        self.store_buttons = [
            Button("Buy Weight ($100)", 100, 450, 200, 50, self.buy_weight, self.font),
            Button("Buy Steroids ($250)", 350, 450, 220, 50, self.buy_steroids, self.font),
            Button("Back to Gym", 600, 450, 150, 50, self.toggle_store, self.font)
        ]

    def draw(self):
        self.screen.fill((30, 30, 30))

        if self.in_store:
            self.draw_store()
        else:
            self.draw_game()

    def draw_game(self):
        for btn in self.buttons:
            btn.draw(self.screen)

        stats = [
            f"Path: {self.player.path.title()}",
            f"Reps: {self.player.reps}",
            f"Weight: {self.player.weight} lbs",
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
        for btn in self.store_buttons:
            btn.draw(self.screen)

        title = self.font.render("🏪 Store", True, (255, 255, 0))
        self.screen.blit(title, (50, 30))

        y = 100
        for key, item in self.store.get_items().items():
            self.screen.blit(self.font.render(f"{item.name} - ${item.cost}", True, (255, 255, 255)), (50, y))
            self.screen.blit(self.font.render(item.description, True, (180, 180, 180)), (50, y + 30))
            y += 70

        bucks_display = self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0))
        self.screen.blit(bucks_display, (50, y))

        message = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(message, (50, y + 40))

    def draw_cooldown_bar(self):
        if not self.game_state.can_rep():
            full_width = 600
            height = 20
            x = 100
            y = 400

            time_left = self.game_state.time_until_next_rep()
            total = self.player.base_rest_time
            fill_ratio = 1 - (time_left / total)

            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, full_width, height))  # Background
            pygame.draw.rect(self.screen, (0, 200, 0), (x, y, int(full_width * fill_ratio), height))  # Fill

    def handle_event(self, event):
        active_buttons = self.store_buttons if self.in_store else self.buttons
        for btn in active_buttons:
            btn.handle_event(event)

    def toggle_store(self):
        self.in_store = not self.in_store
        self.message = ""

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def buy_weight(self):
        self.message = self.store.purchase("weight", self.player)

    def buy_steroids(self):
        self.message = self.store.purchase("steroids", self.player)

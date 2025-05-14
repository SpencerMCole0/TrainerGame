import pygame

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

        self.buttons = [
            Button("Do Rep", 100, 450, 150, 50, self.do_rep, self.font),
            Button("Add Weight", 300, 450, 150, 50, self.add_weight, self.font),
            Button("Use Steroids", 500, 450, 150, 50, self.use_steroids, self.font),
        ]

    def draw(self):
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

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def add_weight(self):
        cost = 100
        if self.player.strength_bucks >= cost:
            self.player.strength_bucks -= cost
            self.player.add_weight()
            self.message = "🏋️‍♂️ Added 5 lbs to barbell!"
        else:
            self.message = "💸 Not enough bucks for weight!"

    def use_steroids(self):
        cost = 250
        if self.player.strength_bucks >= cost:
            self.player.strength_bucks -= cost
            self.player.use_steroids()
            self.message = "💉 Steroids used. Rest time reduced!"
        else:
            self.message = "💸 Not enough bucks for steroids!"


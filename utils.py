# Utility functions like colored output or save/load helpers
import pygame

class Button:
    def __init__(self, x, y, width, height, font, label,
                 callback=None, disabled=False,
                 color=(200, 200, 200), highlight=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.label = label
        self.callback = callback
        self.disabled = disabled
        self.color = color
        self.highlight = highlight

        # Cooldown visuals
        self.cooldown_progress = 1.0  # 0.0 = empty, 1.0 = full
        self.cooldown_active = False

    def update_cooldown(self, progress):
        """Update the visual fill percent (0.0–1.0) for cooldown."""
        self.cooldown_progress = max(0.0, min(1.0, progress))
        self.cooldown_active = self.cooldown_progress < 1.0

    def draw(self, screen):
        # Background color
        base_color = (100, 255, 100) if self.highlight and not self.disabled else self.color
        draw_color = (50, 50, 50) if self.disabled else base_color
        pygame.draw.rect(screen, draw_color, self.rect)

        # Cooldown overlay (fills from left to right)
        if self.cooldown_active and not self.disabled:
            fill_width = int(self.rect.width * self.cooldown_progress)
            cooldown_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
            pygame.draw.rect(screen, (0, 255, 0), cooldown_rect)

        # Button border
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Centered label
        text_surf = self.font.render(self.label, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if self.disabled or self.cooldown_active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.callback:
                self.callback()

# Utility functions like colored output or save/load helpers
class Button:
    def __init__(self, x, y, text, callback, disabled=False, color=None, highlight=False):
        self.text = text
        self.rect = pygame.Rect(x, y, 150, 40)
        self.callback = callback
        self.font = pygame.font.SysFont(None, 24)
        self.color = color if color else (200, 200, 200)
        self.disabled = disabled
        self.highlight = highlight

    def draw(self, screen):
        button_color = self.color if not self.disabled else (100, 100, 100)
        if self.highlight:
            button_color = (180, 255, 180)
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if self.disabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

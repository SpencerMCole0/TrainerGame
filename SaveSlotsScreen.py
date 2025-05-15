import pygame
from utils import Button
import os

class SaveSlotsScreen:
    def __init__(self, screen, game, max_slots=3):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 28)
        self.max_slots = max_slots
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        # Create Back button once
        w, h = self.screen.get_size()
        mid_x = w // 2
        start_y = h // 4
        gap = 60
        self.back_button = Button(mid_x - 100, start_y + self.max_slots * gap + 40, 200, 50, self.font, "Back", self.goto_home)

    def refresh_slots(self):
        w, h = self.screen.get_size()
        mid_x = w // 2
        start_y = h // 4
        gap = 60

        # Clear previous buttons
        self.buttons = []

        for i in range(1, self.max_slots + 1):
            slot_file = f"save_slot{i}.json"
            label = f"Slot {i} - {'Saved' if os.path.exists(slot_file) else 'Empty'}"
            self.buttons.append(Button(mid_x - 100, start_y + (i-1) * gap, 200, 50, self.font, label,
                                       callback=lambda i=i: self.save_slot(i)))

        # Add back button last
        self.buttons.append(self.back_button)

    def draw(self):
        self.refresh_slots()

        self.screen.fill((30, 30, 40))
        title = self.font.render("Select Save Slot", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 40))
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def save_slot(self, slot_num):
        filename = f"save_slot{slot_num}.json"
        self.game.player.save(filename=filename)
        self.game.current_screen = self.game.home_screen  # Exit to home after saving
        self.game.gui.message = f"Game saved to Slot {slot_num} and exited!"

    def goto_home(self):
        self.game.current_screen = self.game.home_screen

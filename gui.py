import pygame
import time
from store import Store
from utils import Button

class GameGUI:
    def open_save_slots(self):
        if self.game:
            self.game.current_screen = self.game.save_slots_screen

    def __init__(self, screen, player, game_state):
        self.screen     = screen
        self.player     = player
        self.game_state = game_state
        self.store      = Store()
        self.store_tab  = "recovery"
        self.in_store   = False
        self.font       = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 40, bold=True)
        self.buttons    = []
        self.message    = ""
        self.game       = None  # will be set in main

        self.slider_dragging = False
        self.slider_track    = None
        self.slider_handle   = None

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_gym()

    def draw_gym(self):
        self.buttons = []
        self.screen.fill((30, 30, 30))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        padding = 30
        line_height = 30

        info = self.player.get_cooldown_debug_info()

        # Career path header (top-left)
        career_surf = self.title_font.render(self.player.path, True, (255, 255, 255))
        career_x = padding
        career_y = padding

        # Buck info (top-right)
        buck_texts = [
            f"GymCoins: {self.player.gym_coins:.2f}",
            f"GymCoins/Rep: {info['GymCoins/Rep']}",
            f"Best Rep/Sec: {info['Best Rep/Sec']}",
            f"Best Daily GC: {info['Best Daily GymCoins']}",
            f"Reset in: {info['Time to Reset']}",
            f"Active Rem: {info['Active Remaining']}s",
        ]
        buck_surfs = [self.font.render(t, True, (255, 255, 255)) for t in buck_texts]

        # Weight info (bottom-left)
        weight_texts = [
            f"Reps: {info['Reps']}",
            f"Total Owned Weight: {self.player.total_weight:.1f} kg",
        ]
        weight_surfs = [self.font.render(t, True, (255, 255, 255)) for t in weight_texts]

        # Cooldown info (bottom-right)
        cooldown_texts = [
            f"Cooldown: {info['Cooldown Time']}s",
            f"Rest Reduction: {info['Rest Reduction']}s",
            f"Min Rest Cap: {'YES' if info['Min Rest Cap Hit'] else 'No'}",
        ]
        cooldown_surfs = [self.font.render(t, True, (255, 255, 255)) for t in cooldown_texts]

        # Determine whether to show a message line (and highlight rep results)
        has_message = bool(self.message and self.message.strip())
        message_color = (255, 255, 255)
        if has_message and "rep" in self.message.lower():
            message_color = (255, 215, 0)

        # Layout constants
        btn_w, btn_h = 120, 40
        gap = 40
        barbell_w, barbell_h = 300, 60
        slider_w, slider_h = 200, 8
        block_gap = 80

        # Heights
        top_left_h = career_surf.get_height()
        top_right_h = len(buck_surfs) * line_height
        top_section_height = max(top_left_h, top_right_h)

        weight_block_height = len(weight_surfs) * line_height + slider_h + 40  # include extra padding before slider
        cooldown_block_height = len(cooldown_surfs) * line_height
        bottom_section_height = max(weight_block_height, cooldown_block_height)

        message_height = line_height if has_message else 0
        button_group_height = btn_h * 2 + gap

        total_height = (
            top_section_height
            + 30  # spacing between top info and barbell
            + barbell_h
            + 30  # spacing between barbell and bottom info
            + bottom_section_height
            + 30  # spacing between bottom info and buttons
            + message_height
            + 30  # spacing between message and buttons
            + button_group_height
        )

        y_base = max(padding, (screen_h - total_height) // 2)

        # Draw career header
        self.screen.blit(career_surf, (career_x, y_base))

        # Draw bucks info (top-right)
        bucks_w = max(s.get_width() for s in buck_surfs)
        bucks_x = screen_w - padding - bucks_w
        y_bucks = y_base
        for surf in buck_surfs:
            self.screen.blit(surf, (bucks_x, y_bucks))
            y_bucks += line_height

        # Determine barbell position
        barbell_x = (screen_w - barbell_w) // 2
        barbell_y = y_base + top_section_height + 30

        # Bottom-left: weights + slider
        weights_w = max(s.get_width() for s in weight_surfs)
        weights_x = barbell_x - block_gap - weights_w
        y_weights = barbell_y + barbell_h + 30
        for surf in weight_surfs:
            self.screen.blit(surf, (weights_x, y_weights))
            y_weights += line_height

        # Add extra spacing before the slider so it doesn't overlap the weight text
        y_weights += 40
        slider_x = weights_x
        slider_y = y_weights
        pygame.draw.rect(self.screen, (100, 100, 100), (slider_x, slider_y, slider_w, slider_h))
        t = (self.player.barbell_weight - self.player.base_bar_weight) / (self.player.total_weight - self.player.base_bar_weight) if self.player.total_weight > self.player.base_bar_weight else 0
        handle_x = slider_x + t * slider_w
        handle_y = slider_y + slider_h // 2
        pygame.draw.circle(self.screen, (200, 200, 0), (int(handle_x), int(handle_y)), 12)
        self.slider_track = pygame.Rect(slider_x, slider_y, slider_w, slider_h)
        self.slider_handle = pygame.Rect(int(handle_x) - 12, int(handle_y) - 12, 24, 24)

        wt_label = self.font.render(f"Barbell Weight: {self.player.barbell_weight:.1f} kg", True, (255, 255, 255))
        self.screen.blit(wt_label, (slider_x, slider_y - 30))

        # Bottom-right: cooldown info
        cooldown_w = max(s.get_width() for s in cooldown_surfs)
        cooldown_x = barbell_x + barbell_w + block_gap
        y_cooldown = barbell_y + barbell_h + 30
        for surf in cooldown_surfs:
            self.screen.blit(surf, (cooldown_x, y_cooldown))
            y_cooldown += line_height

        # Message line (colored for relevant rep feedback)
        if has_message:
            y_msg = barbell_y + barbell_h + 30 + bottom_section_height + 10
            msg_prefix = self.font.render("Message: ", True, (255, 255, 255))
            msg_body = self.font.render(self.message, True, message_color)
            msg_total_w = msg_prefix.get_width() + msg_body.get_width()
            msg_x = (screen_w - msg_total_w) // 2
            self.screen.blit(msg_prefix, (msg_x, y_msg))
            self.screen.blit(msg_body, (msg_x + msg_prefix.get_width(), y_msg))

        # Draw centered barbell
        self.draw_barbell(barbell_x, barbell_y)

        # Position buttons beneath the barbell (and message)
        y_buttons = barbell_y + barbell_h + 30 + bottom_section_height + (line_height if has_message else 0) + 30
        btn_group_w = btn_w * 2 + gap
        btn_x = (screen_w - btn_group_w) // 2
        btn_y = y_buttons

        # Cooldown progress
        if self.game_state:
            time_since_rep = time.time() - self.game_state.last_rep_time
            cooldown_time = self.player.get_current_rest_time()
            progress = min(time_since_rep / cooldown_time, 1.0)
        else:
            progress = 1.0

        can_rep = self.game_state.can_rep() if self.game_state else True
        do_rep_btn = Button(btn_x, btn_y, btn_w, btn_h, self.font, "Do Rep", self.do_rep, disabled=not can_rep)
        do_rep_btn.update_cooldown(progress)

        self.buttons.append(do_rep_btn)
        self.buttons.append(Button(btn_x + btn_w + gap, btn_y, btn_w, btn_h, self.font, "Open Store", self.open_store))
        self.buttons.append(Button(btn_x, btn_y + btn_h + gap, btn_w, btn_h, self.font, "Save & Exit", self.save_and_exit))
        self.buttons.append(Button(btn_x + btn_w + gap, btn_y + btn_h + gap, btn_w, btn_h, self.font, "Exit to Menu", self.exit_to_menu))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        padding = 30
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        self.screen.blit(self.large_font.render("🏪 Store", True, (255, 255, 0)), (padding, padding))
        bucks = self.font.render(f"Your GymCoins: {self.player.gym_coins:.2f}", True, (0, 255, 0))
        self.screen.blit(bucks, (screen_w - padding - bucks.get_width(), padding))

        extra_v = 20
        tabs_y = padding + self.large_font.get_height() + extra_v

        # Make the tab buttons centered across the screen so layout scales to different window sizes
        tab_btn_w, tab_btn_h = 150, 40
        tab_gap = 20
        total_tabs_w = 4 * tab_btn_w + 3 * tab_gap
        tabs_start_x = max(padding, (screen_w - total_tabs_w) // 2)

        self.buttons = [
            Button(tabs_start_x, tabs_y, tab_btn_w, tab_btn_h, self.font, "🧃 Recovery", callback=lambda: self.set_tab("recovery"), highlight=(self.store_tab == "recovery")),
            Button(tabs_start_x + (tab_btn_w + tab_gap) * 1, tabs_y, tab_btn_w, tab_btn_h, self.font, "📢 Sponsorships", callback=lambda: self.set_tab("sponsorship"), highlight=(self.store_tab == "sponsorship")),
            Button(tabs_start_x + (tab_btn_w + tab_gap) * 2, tabs_y, tab_btn_w, tab_btn_h, self.font, "🏃 Trainers", callback=lambda: self.set_tab("trainers"), highlight=(self.store_tab == "trainers")),
            Button(tabs_start_x + (tab_btn_w + tab_gap) * 3, tabs_y, tab_btn_w, tab_btn_h, self.font, "🏋️ Weights", callback=lambda: self.set_tab("weights"), highlight=(self.store_tab == "weights")),
        ]

        # Ensure item text is drawn below the tab buttons to avoid overlap
        # Note: item cost text is drawn 50px above the button, so we add enough top padding.
        items_start_y = tabs_y + tab_btn_h + 70
        all_items = self.store.get_items()
        rec, spon, trainers, wts = self.store.get_grouped_items()
        keys = {"recovery": rec, "sponsorship": spon, "trainers": trainers, "weights": wts}[self.store_tab]
        items = [all_items[k] for k in keys]

        cols = 4
        col_width = (screen_w - 2 * padding) // cols
        row_height = tab_btn_h + 90

        for idx, item in enumerate(items):
            col = idx % cols
            row = idx // cols
            x = padding + col * col_width
            y = items_start_y + row * row_height

            cost_surf = self.font.render(f"Cost: {item.cost:.0f} GC", True, (255, 255, 0))
            self.screen.blit(cost_surf, (x, y - 50))
            desc_surf = self.font.render(item.description, True, (255, 255, 255))
            self.screen.blit(desc_surf, (x, y - 30))

            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED"
            if not maxed:
                # Extract the amount from the action lambda (defaults or closure).
                amt = None
                if getattr(item.action, "__defaults__", None):
                    amt = item.action.__defaults__[0]
                elif getattr(item.action, "__closure__", None):
                    amt = item.action.__closure__[0].cell_contents

                if self.store_tab == "sponsorship" and amt is not None:
                    label = f"Buy (+${amt}/rep)"
                elif self.store_tab == "recovery" and amt is not None:
                    label = f"Buy (-{amt}s)"
                else:
                    label = f"Buy ({item.times_bought}/{item.limit})"

            disabled = maxed or not item.can_buy(self.player)[0]
            self.buttons.append(Button(x, y, 160, 40, self.font, label, callback=lambda it=item: self.purchase(it), disabled=disabled))

        # Back button
        back_w, back_h = 160, 40
        bx = screen_w - back_w - padding
        by = screen_h - back_h - padding
        self.buttons.append(Button(bx, by, back_w, back_h, self.font, "Back to Gym", callback=self.go_to_gym, color=(255, 100, 100)))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_barbell(self, x, y):
        BAR_LENGTH = 300
        BAR_HEIGHT = 20
        BASE_BAR_COLOR = (180, 180, 180)
        COLLAR_COLOR = (120, 120, 120)
        PLATE_COLORS = {
            0.5: (150, 150, 150),
            1: (100, 100, 255),
            2: (255, 255, 100),
            2.5: (255, 165, 0),
            5: (255, 0, 0),
            10: (0, 0, 255),
            15: (0, 255, 0),
            20: (255, 255, 255),
            25: (0, 0, 0)
        }
        PLATE_WIDTH = 15
        PLATE_HEIGHT = 50

        pygame.draw.rect(self.screen, BASE_BAR_COLOR, (x, y, BAR_LENGTH, BAR_HEIGHT))
        collar_w, collar_h = 40, 60
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x - collar_w, y - 20, collar_w, collar_h))
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x + BAR_LENGTH, y - 20, collar_w, collar_h))

        plate_x = x - collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            for _ in range(self.player.plates[weight]):
                plate_x -= PLATE_WIDTH
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - 15, PLATE_WIDTH, PLATE_HEIGHT))

        plate_x = x + BAR_LENGTH + collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            for _ in range(self.player.plates[weight]):
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - 15, PLATE_WIDTH, PLATE_HEIGHT))
                plate_x += PLATE_WIDTH

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.slider_handle and self.slider_handle.collidepoint(event.pos):
            self.slider_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.slider_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.slider_dragging:
            mx, _ = event.pos
            if self.slider_track:
                clamped = max(self.slider_track.x, min(mx, self.slider_track.x + self.slider_track.w))
                t = (clamped - self.slider_track.x) / self.slider_track.w
                min_wt = self.player.base_bar_weight
                max_wt = self.player.total_weight
                new_wt = min_wt + t * (max_wt - min_wt)
                snapped = round((new_wt - min_wt) / 5) * 5 + min_wt
                self.player.barbell_weight = max(min_wt, min(snapped, max_wt))

        for btn in self.buttons:
            btn.handle_event(event)

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def purchase(self, item):
        self.message = item.buy(self.player)

    def save_and_exit(self):
        if self.game:
            self.game.current_screen = self.game.save_slots_screen
        self.message = ""

    def open_store(self):
        self.in_store = True
        self.message = ""

    def exit_to_menu(self):
        if self.game:
            self.game.current_screen = self.game.home_screen
        self.message = ""

    def set_tab(self, tab):
        self.store_tab = tab
        self.message = ""

    def go_to_gym(self):
        self.in_store = False
        self.message = ""

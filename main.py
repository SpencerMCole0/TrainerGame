import pygame
from gui import GameGUI
from player import Player
from game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("TrainerGame")

    # Default career path for now
    career_path = "weightlifting"
    player = Player(career_path)
    game_state = GameState(player)
    gui = GameGUI(screen, player, game_state)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((30, 30, 30))
        gui.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                gui.screen = screen  # Update GUI's reference to new screen size
            gui.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

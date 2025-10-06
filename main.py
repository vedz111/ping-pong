import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        events = pygame.event.get()  # collect events ONCE

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        pygame.display.flip()

        # now handle game over / replay input using same events
        engine.check_game_over(SCREEN, events)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
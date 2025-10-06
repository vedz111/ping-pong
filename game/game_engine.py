import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5  # Default to Best of 5
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 40)
        self.game_over = False
        self.winner_text = ""
        self.in_replay_menu = False

    def handle_input(self):
        if self.game_over:
            return  # ignore paddle input during game over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Skip updates if in menu or game is over
        if self.game_over or self.in_replay_menu:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over_condition()

    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Game over / replay UI
        if self.game_over:
            self.render_game_over(screen)
        elif self.in_replay_menu:
            self.render_replay_menu(screen)

    def render_game_over(self, screen):
        # Show winner message
        text_surface = self.game_over_font.render(self.winner_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(text_surface, text_rect)

        # After showing winner, display replay menu options
        menu_text = self.font.render("Press any key to continue...", True, WHITE)
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(menu_text, menu_rect)

    def render_replay_menu(self, screen):
        title = self.menu_font.render("Select Match Type:", True, WHITE)
        options = [
            "Press 3 - Best of 3",
            "Press 5 - Best of 5",
            "Press 7 - Best of 7",
            "Press ESC - Exit"
        ]
        screen.blit(title, (self.width // 2 - 150, self.height // 2 - 100))
        for i, text in enumerate(options):
            option_surface = self.font.render(text, True, WHITE)
            screen.blit(option_surface, (self.width // 2 - 120, self.height // 2 - 40 + i * 40))

    def check_game_over_condition(self):
        if self.player_score >= self.target_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.target_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def check_game_over(self, screen, events):
        # If game just ended, wait briefly, then show replay options
        if self.game_over:
            self.render(screen)
            pygame.display.flip()
            pygame.time.delay(1500)
            self.game_over = False
            self.in_replay_menu = True

        # If we’re in replay menu, wait for user input
        if self.in_replay_menu:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.start_new_match(target=3)
                    elif event.key == pygame.K_5:
                        self.start_new_match(target=5)
                    elif event.key == pygame.K_7:
                        self.start_new_match(target=7)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    def start_new_match(self, target):
        """Reset everything and start a new round."""
        self.target_score = target
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
        self.in_replay_menu = False
        self.game_over = False
        self.winner_text = ""
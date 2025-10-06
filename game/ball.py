import pygame
import random
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Initialize the mixer only once globally, not per instance
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Locate sounds in /sounds folder (1 level up from /game)
        base_path = os.path.dirname(os.path.dirname(__file__))
        sounds_path = os.path.join(base_path, "sounds")

        # Load sounds safely
        self.paddle_hit_sound = self.load_sound(os.path.join(sounds_path, "paddle_hit.wav"))
        self.wall_bounce_sound = self.load_sound(os.path.join(sounds_path, "wall_bounce.wav"))
        self.score_sound = self.load_sound(os.path.join(sounds_path, "score.wav"))

    def load_sound(self, filepath):
        """Safely load a sound file; return None if not found."""
        if os.path.exists(filepath):
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(0.6)  # Slightly reduced volume for balance
                return sound
            except pygame.error as e:
                print(f"⚠️ Error loading sound {filepath}: {e}")
        else:
            print(f"⚠️ Warning: Sound file not found: {filepath}")
        return None

    def move(self):
        """Move the ball and handle top/bottom wall bounces."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce on top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.wall_bounce_sound:
                self.wall_bounce_sound.play()

    def check_collision(self, player, ai):
        """Check and handle collision with paddles."""
        ball_rect = self.rect()

        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width + 1  # avoid sticking
            self.velocity_x = abs(self.velocity_x)
            if self.paddle_hit_sound:
                self.paddle_hit_sound.play()

        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width - 1
            self.velocity_x = -abs(self.velocity_x)
            if self.paddle_hit_sound:
                self.paddle_hit_sound.play()

    def reset(self):
        """Reset the ball to the center and play scoring sound."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if self.score_sound:
            self.score_sound.play()

    def rect(self):
        """Return the pygame.Rect for the ball."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
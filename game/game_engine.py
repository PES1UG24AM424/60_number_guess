import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # Task 2: Dynamic search range
        self.min_range = 1
        self.max_range = 100

        # Task 3: Recent guess history
        self.guess_history = []

        # Task 4: Maximum attempts
        self.max_attempts = 10
        self.game_over = False

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False

        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        # Task 1: Prevent empty input from crashing
        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number!"
            self.feedback_color = (240, 220, 80)
            return

        guess = int(self.input_box.text)

        self.attempts += 1
        self.input_box.clear()

        # Task 3: Add guess to recent history
        self.guess_history.append(guess)
        self.guess_history = self.guess_history[-5:]

        if guess < self.secret_number:
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

            # Task 2: Narrow the lower boundary
            self.min_range = guess + 1

        elif guess > self.secret_number:
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

            # Task 2: Narrow the upper boundary
            self.max_range = guess - 1

        else:
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True
            return

        # Task 4: Check maximum attempts
        if self.attempts >= self.max_attempts:
            self.game_over = True
            self.feedback_msg = (
                f"GAME OVER! The number was {self.secret_number}."
            )
            self.feedback_color = (240, 80, 80)

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_range = 1
        self.max_range = 100
        self.guess_history = []
        self.game_over = False
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (self.width // 2 - title_surf.get_width() // 2, 35)
        )

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.max_attempts}",
            True,
            (180, 185, 195)
        )
        screen.blit(
            attempts_surf,
            (self.width // 2 - attempts_surf.get_width() // 2, 95)
        )

        # Task 2: Display current possible range
        range_surf = self.font_medium.render(
            f"Possible range: {self.min_range} - {self.max_range}",
            True,
            (200, 210, 220)
        )
        screen.blit(
            range_surf,
            (self.width // 2 - range_surf.get_width() // 2, 125)
        )

        self.input_box.render(screen)

        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6
        )
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )
        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2
            )
        )

        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )
        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                235
            )
        )

        # Task 3: Display recent guess history
        history_text = "Recent guesses: " + ", ".join(
            str(g) for g in self.guess_history
        )

        history_surf = self.font_medium.render(
            history_text,
            True,
            (190, 200, 210)
        )
        screen.blit(
            history_surf,
            (
                self.width // 2 - history_surf.get_width() // 2,
                340
            )
        )

        # Task 4: Display restart message after game ends
        if self.game_won or self.game_over:
            restart_surf = self.font_medium.render(
                "Press [R] to Start a New Game",
                True,
                (255, 220, 80)
            )
            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    295
                )
            )
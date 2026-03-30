import sys
import pygame
import chess
import pygame.freetype
from testing import *
from BlockedScreen import *
from SettingsScreen import *

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# ---------------- MenuScreen ----------------
class MenuScreen:
    """Main menu screen with options to play, settings, or quit."""

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.title_font = app.title_font
        self.text_font = app.text_font
        self.clock = pygame.time.Clock()

        # Main menu buttons
        self.buttons = {
            "Vs Friend": pygame.Rect(WIDTH // 2 - 150, 250, 300, 60),
            "Vs AI": pygame.Rect(WIDTH // 2 - 150, 340, 300, 60),
            "Tutorial": pygame.Rect(WIDTH // 2 - 150, 430, 300, 60),
            "Settings": pygame.Rect(WIDTH // 2 - 150, 520, 300, 60),
            "Quit": pygame.Rect(WIDTH // 2 - 150, 610, 300, 60),
        }

    def run(self):
        """Main menu loop."""
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            # Draw title
            title_surf, title_rect = self.title_font.render("Chess", TITLE_COLOR)
            title_rect.center = (WIDTH // 2, 120)
            self.screen.blit(title_surf, title_rect)

            # Draw buttons
            for text, rect in self.buttons.items():
                self.draw_button(rect, text, mouse_pos)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for label, rect in self.buttons.items():
                        if rect.collidepoint(event.pos):
                            if label == "Vs Friend":
                                return self.choose_friend_mode()
                            elif label == "Vs AI":
                                return "blocked_ai"
                            elif label == "Tutorial":
                                return "blocked_tutorial"
                            elif label == "Settings":
                                return "settings"
                            elif label == "Quit":
                                return "quit"

            self.clock.tick(60)

    def choose_friend_mode(self):
        """Sub-menu for Full or Half board."""
        buttons = {
            "Full Board": pygame.Rect(WIDTH // 2 - 150, 300, 300, 60),
            "Half Board": pygame.Rect(WIDTH // 2 - 150, 400, 300, 60),
            "Back": pygame.Rect(WIDTH // 2 - 150, 500, 300, 60),
        }

        running = True
        next_action = "menu"  # default fallback

        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            # Draw sub-menu title
            title_surf, title_rect = self.title_font.render("Choose Board Mode", TITLE_COLOR)
            title_rect.center = (WIDTH // 2, 150)
            self.screen.blit(title_surf, title_rect)

            # Draw buttons
            for text, rect in buttons.items():
                self.draw_button(rect, text, mouse_pos)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for label, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            if label == "Full Board":
                                next_action = "play_friend_full"
                                running = False
                            elif label == "Half Board":
                                next_action = "play_friend_half"
                                running = False
                            elif label == "Back":
                                next_action = "menu"
                                running = False

            pygame.time.Clock().tick(60)  # keep loop stable

        return next_action

    def draw_button(self, rect, text, mouse_pos):
        """Helper to draw a button with hover effect."""
        color = (118, 150, 86)
        if rect.collidepoint(mouse_pos):
            color = (150, 180, 120)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        surf, rect_text = self.text_font.render(text, (255, 255, 255))
        rect_text.center = rect.center
        self.screen.blit(surf, rect_text)

# ---------------- GameApp ----------------
class GameApp:
    """Manages main loop, screens, and settings."""

    def __init__(self):
        pygame.init()
        pygame.freetype.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        # Fonts
        self.title_font = pygame.freetype.SysFont("Arial", 64, bold=True)
        self.text_font = pygame.freetype.SysFont("Arial", 24)

        # Settings
        self.settings = {
            "highlight_legal_moves": True
        }

        self.running = True

    def run(self):
        current_screen = MenuScreen(self)

        while self.running:
            next_screen = current_screen.run()

            # Handle screen transitions
            if next_screen == "quit":
                self.running = False
            elif next_screen == "settings":
                current_screen = SettingsScreen(self)
            elif next_screen == "play_friend_full":
                current_screen = PlaySession(self, mode="Full Board")
            elif next_screen == "play_friend_half":
                current_screen = PlaySession(self, mode="Half Board")
            elif next_screen == "blocked_ai":
                current_screen = BlockedScreen(self, "Vs AI")
            elif next_screen == "blocked_tutorial":
                current_screen = BlockedScreen(self, "Tutorial")
            else:
                current_screen = MenuScreen(self)

        pygame.quit()
        sys.exit()

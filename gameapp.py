import sys
import pygame
import pygame.freetype
from BlockedScreen import *
from MenuScreen import *
from PlaySession import *
from SettingsScreen import *

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Window constants
WIDTH, HEIGHT = 640, 700

class GameApp:
#  Manages the overall game lifecycle, window, fonts, and screen switching.
    def __init__(self):
        # Initialize pygame modules
        pygame.init()
        pygame.freetype.init()

        # Window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        # Fonts used throughout the program
        self.title_font = pygame.freetype.SysFont("Arial", 64, bold=True)
        self.text_font = pygame.freetype.SysFont("Arial", 24)

        # Shared user settings (can toggle from settings screen)
        self.settings = {
            "highlight_legal_moves": True,
            "show_half_board": False
        }

        # Game state
        self.running = True

    def run(self):
        # Controls main loop and screen transitions.
        current_screen = MenuScreen(self)

        while self.running:
            next_screen = current_screen.run()  # Each screen must return a next action

            # Handle transitions
            if next_screen == "quit":
                self.running = False
            elif next_screen == "settings":
                current_screen = SettingsScreen(self)
            elif next_screen == "play_friend_full":
                current_screen = PlaySession(self, mode="Full Board")
            elif next_screen == "play_friend_half":
                current_screen = PlaySession(self, mode="Half Board")
            elif next_screen == "play_ai":
                current_screen = PlaySession(self, mode="Vs AI")
            elif next_screen == "blocked_ai":
                current_screen = BlockedScreen(self, "Vs AI")
            elif next_screen == "blocked_tutorial":
                current_screen = BlockedScreen(self, "Tutorial")
            else:
                # Default fallback
                current_screen = MenuScreen(self)

        pygame.quit()
        sys.exit()

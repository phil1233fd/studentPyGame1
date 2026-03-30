import sys
import pygame
import chess
import pygame.freetype
from gameapp import *

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# ---------------- Helper Function ----------------
def draw_button(screen, rect, text, mouse_pos, font, color=(118, 150, 86), hover_color=(150, 180, 120)):
    """Draws a rounded rectangle button that darkens when hovered."""
    hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if hovered else color, rect, border_radius=12)
    text_surf, text_rect = font.render(text, (255, 255, 255))
    text_rect.center = rect.center
    screen.blit(text_surf, text_rect)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = GameApp()
    app.run()
import sys
import pygame
import pygame.freetype

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

class SettingsScreen:
    """
    Handles the settings menu UI, toggles, and user interactions.
    """
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.settings = app.settings
        self.button_font = app.text_font
        self.WIDTH, self.HEIGHT = app.screen.get_size()
        self.BG_COLOR = (48, 46, 43)
        self.TEXT_COLOR = (255, 255, 255)

        # UI rectangles
        self.highlight_rect = pygame.Rect(self.WIDTH//2 - 100, self.HEIGHT//2 - 40, 200, 60)
        self.back_rect = pygame.Rect(20, self.HEIGHT - 60, 120, 40)

    def draw_button(self, rect, text, mouse_pos):
        color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (64, 64, 60)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        text_surf, text_rect = self.button_font.render(text, self.TEXT_COLOR)
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(self.BG_COLOR)

            # Title
            title_font = pygame.freetype.SysFont("Arial", 60)
            title_surf, title_rect = title_font.render("Settings", self.TEXT_COLOR)
            title_rect.center = (self.WIDTH//2, 80)
            self.screen.blit(title_surf, title_rect)

            # Highlight Legal Moves toggle
            toggle_color = (0, 200, 0) if self.settings["highlight_legal_moves"] else (200, 0, 0)
            pygame.draw.rect(self.screen, toggle_color, self.highlight_rect, border_radius=10)

            # Text
            line1 = "Highlight Legal Moves"
            line2 = "ON" if self.settings["highlight_legal_moves"] else "OFF"
            text_surf1, text_rect1 = self.button_font.render(line1, self.TEXT_COLOR)
            text_rect1.centerx = self.highlight_rect.centerx
            text_rect1.y = self.highlight_rect.y + 5
            self.screen.blit(text_surf1, text_rect1)

            text_surf2, text_rect2 = self.button_font.render(line2, self.TEXT_COLOR)
            text_rect2.centerx = self.highlight_rect.centerx
            text_rect2.y = self.highlight_rect.y + self.highlight_rect.height//2
            self.screen.blit(text_surf2, text_rect2)

            # Back button
            self.draw_button(self.back_rect, "Back", mouse_pos)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.highlight_rect.collidepoint(event.pos):
                        self.settings["highlight_legal_moves"] = not self.settings["highlight_legal_moves"]
                    elif self.back_rect.collidepoint(event.pos):
                        running = False
        return "menu"
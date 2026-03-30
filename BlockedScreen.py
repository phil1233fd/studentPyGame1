import sys
import pygame
import pygame.freetype

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

class BlockedScreen:
    """
    A screen that displays a message saying the feature is blocked by the school.
    """
    def __init__(self, app, feature_name):
        self.app = app
        self.screen = app.screen
        self.title_font = app.title_font
        self.text_font = app.text_font
        self.feature_name = feature_name
        self.clock = pygame.time.Clock()

        # Back button rectangle
        self.back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 60)

    def draw_button(self, rect, text, mouse_pos):
        hovered = rect.collidepoint(mouse_pos)
        color = (30, 30, 30) if not hovered else (100, 100, 100)
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        text_surf, text_rect = self.text_font.render(text, (255, 255, 255))
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            # Title
            title_surf, title_rect = self.title_font.render(self.feature_name, (255, 255, 255))
            title_rect.center = (WIDTH // 2, 200)
            self.screen.blit(title_surf, title_rect)

            # Blocked message
            msg = "This feature has been blocked by the school."
            msg_surf, msg_rect = self.text_font.render(msg, (255, 255, 255))
            msg_rect.center = (WIDTH // 2, 340)
            self.screen.blit(msg_surf, msg_rect)

            # Draw Back button
            self.draw_button(self.back_button, "Back", mouse_pos)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return "menu"

            self.clock.tick(60)
import pygame
import chess
# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# ------------------- Load Chess Piece Images -------------------
# Black pieces
PB = pygame.image.load("Pawn-black-classical.png")
NB = pygame.image.load("Knight-black-classic.png")
RB = pygame.image.load("Rook-black-classical.png")
BB = pygame.image.load("Bishop-black-classical.png")
QB = pygame.image.load("Queen-black-classical.png")
KB = pygame.image.load("King-black-classical.png")

# White pieces
PW = pygame.image.load("Pawn-white-classical.png")
NW = pygame.image.load("Knight-white-classic.png")
RW = pygame.image.load("Rook-white-classical.png")
BW = pygame.image.load("Bishop-white-classical.png")
QW = pygame.image.load("Queen-white-classical.png")
KW = pygame.image.load("King-white-classical.png")


class ChessBoardUI:
    """
    Handles drawing the chessboard, pieces, highlights, and animations.
    """

    def __init__(self, screen, width, height, square_size=80):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.SQUARE_SIZE = square_size

        # Colors
        self.LIGHT_SQUARE = (238, 238, 210)
        self.DARK_SQUARE = (118, 150, 86)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 100)
        self.LAST_MOVE_COLOR = (70, 130, 180, 100)

        # Fonts
        self.font = pygame.freetype.SysFont("Segoe UI Symbol", 40)

        # Piece images mapping
        self.UNICODE_PIECES = {
            "P": PW, "N": NW, "B": BW, "R": RW, "Q": QW, "K": KW,
            "p": PB, "n": NB, "b": BB, "r": RB, "q": QB, "k": KB
        }

    # ------------------- Drawing the Board -------------------
    def draw_board(self, board, selected_square=None, prev_move=None, last_move=None, mode="Vs Friend"):
        visible_files = range(5) if mode == "Half Board" else range(8)
        cols = len(visible_files)
        rows = 8
        square_size = self.WIDTH // 8
        self.SQUARE_SIZE = square_size

        total_board_width = square_size * cols
        x_offset = (self.WIDTH - total_board_width) // 2
        y_offset = (self.HEIGHT - square_size * rows - 60) // 2

        for rank in range(8):
            for file_index, file in enumerate(visible_files):
                color = self.LIGHT_SQUARE if (rank + file) % 2 == 0 else self.DARK_SQUARE
                rect = pygame.Rect(
                    x_offset + file_index * square_size,
                    y_offset + rank * square_size,
                    square_size,
                    square_size
                )
                pygame.draw.rect(self.screen, color, rect)

    # ------------------- Drawing Pieces -------------------
    def draw_pieces(self, board, use_png=True, mode="Vs Friend"):
        visible_files = range(5) if mode == "Half Board" else range(8)
        square_size = self.WIDTH // 8
        total_board_width = square_size * len(visible_files)
        x_offset = (self.WIDTH - total_board_width) // 2
        y_offset = (self.HEIGHT - square_size * 8 - 60) // 2

        for square, piece in board.piece_map().items():
            rank = 7 - chess.square_rank(square)
            file = chess.square_file(square)

            # Skip hidden columns in Half Board mode
            if mode == "Half Board" and file >= 5:
                continue

            file_index = list(visible_files).index(file) if mode == "Half Board" else file
            pos_x = x_offset + file_index * square_size + square_size // 2
            pos_y = y_offset + rank * square_size + square_size // 2

            if use_png:
                self.draw_piece_png(piece, pos_x, pos_y, square_size)
            else:
                self.draw_piece_symbol(piece, pos_x, pos_y)

    def draw_piece_png(self, piece, pos_x, pos_y, square_size):
        """Draws a PNG chess piece centered on the given position."""
        if piece is None:
            return
        image = self.get_piece_image(piece)
        if image:
            image = pygame.transform.smoothscale(image, (square_size, square_size))
            rect = image.get_rect(center=(pos_x, pos_y))
            self.screen.blit(image, rect)

    def get_piece_image(self, piece):
        """Returns the corresponding piece image."""
        return self.UNICODE_PIECES.get(piece.symbol(), None)

    # ------------------- Valid Moves Highlight -------------------
    def draw_valid_moves(self):
        if not self.app.settings.get("highlight_legal_moves", True):
            return

        square_size = self.ui.SQUARE_SIZE
        visible_files = range(5) if self.mode == "Half Board" else range(8)
        cols = len(visible_files)
        rows = 8
        total_board_width = square_size * cols
        x_offset = (self.WIDTH - total_board_width) // 2
        y_offset = (self.HEIGHT - square_size * rows - 60) // 2

        for move in self.valid_moves:
            row = 7 - chess.square_rank(move.to_square)
            col = chess.square_file(move.to_square)

            if self.mode == "Half Board" and col >= 5:
                continue

            file_index = list(visible_files).index(col) if self.mode == "Half Board" else col
            pos_x = x_offset + file_index * square_size + square_size // 2
            pos_y = y_offset + row * square_size + square_size // 2

            pygame.draw.circle(self.screen, (255, 0, 0), (pos_x, pos_y), 15)

    # ------------------- Mouse to Square Mapping -------------------
    def get_square_from_mouse(self, pos, mode="Vs Friend"):
        x, y = pos
        square_size = self.SQUARE_SIZE
        visible_files = range(5) if mode == "Half Board" else range(8)
        cols = len(visible_files)
        rows = 8
        total_board_width = square_size * cols
        x_offset = (self.WIDTH - total_board_width) // 2
        y_offset = (self.HEIGHT - square_size * rows - 60) // 2

        # Check if click is inside visible board area
        if not (x_offset <= x < x_offset + total_board_width) or not (y_offset <= y < y_offset + square_size * rows):
            return None

        file_index = int((x - x_offset) // square_size)
        col = list(visible_files)[file_index]
        row = int((y - y_offset) // square_size)
        rank = 7 - row
        return chess.square(col, rank)

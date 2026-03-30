import sys
import pygame
import chess
import pygame.freetype
from ChessBoardUI import *

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# ---------- Load PNGs ----------
PB = pygame.image.load("Pawn-black-classical.png")
NB = pygame.image.load("Knight-black-classic.png")
RB = pygame.image.load("Rook-black-classical.png")
BB = pygame.image.load("Bishop-black-classical.png")
QB = pygame.image.load("Queen-black-classical.png")
KB = pygame.image.load("King-black-classical.png")

PW = pygame.image.load("Pawn-white-classical.png")
NW = pygame.image.load("Knight-white-classic.png")
RW = pygame.image.load("Rook-white-classical.png")
BW = pygame.image.load("Bishop-white-classical.png")
QW = pygame.image.load("Queen-white-classical.png")
KW = pygame.image.load("King-white-classical.png")


class PlaySession:
    """
    Handles a chess game session (Player vs Player only).
    Supports full or half-board mode.
    """

    def __init__(self, app, mode="Vs Friend"):
        self.app = app
        self.screen = app.screen
        self.WIDTH, self.HEIGHT = app.screen.get_size()
        self.mode = mode

        # UI setup
        self.ui = ChessBoardUI(self.screen, self.WIDTH, self.HEIGHT)
        self.ui = ChessBoardUI(self.screen, WIDTH, HEIGHT)
        self.SQUARE_SIZE = self.ui.SQUARE_SIZE

        # Piece images mapping
        self.pieces_images = {
            'Pw': PW, 'Pb': PB,
            'Rw': RW, 'Rb': RB,
            'Nw': NW, 'Nb': NB,
            'Bw': BW, 'Bb': BB,
            'Qw': QW, 'Qb': QB,
            'Kw': KW, 'Kb': KB,
        }

        # ---------- BOARD SETUP ----------
        if mode == "Half Board":
            self.setup_half_board()
        else:
            self.board = chess.Board()  # full board

        # ---------- Bottom buttons ----------
        self.TAB_HEIGHT = self.HEIGHT - 640
        self.undo_rect = pygame.Rect(20, 650, 120, 40)
        self.draw_rect = pygame.Rect(160, 650, 120, 40)
        self.menu_rect = pygame.Rect(300, 650, 140, 40)
        self.review_rect = pygame.Rect(450, 650, 170, 40)

        # ---------- Game state ----------
        self.move_history = []
        self.selected_square = None
        self.previous_move = None
        self.last_move_squares = None
        self.valid_moves = []
        self.running = True

    # ---------------- Half Board Setup ----------------
    def setup_half_board(self):
        """Set up half-board: pawns + king, queen, rook, knight, bishop."""
        self.board = chess.Board(None)  # empty board

        # White pawns
        for file in range(8):
            self.board.set_piece_at(chess.square(file, 1), chess.Piece(chess.PAWN, chess.WHITE))
        # White major pieces
        self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        self.board.set_piece_at(chess.D1, chess.Piece(chess.QUEEN, chess.WHITE))
        self.board.set_piece_at(chess.A1, chess.Piece(chess.ROOK, chess.WHITE))
        self.board.set_piece_at(chess.B1, chess.Piece(chess.KNIGHT, chess.WHITE))
        self.board.set_piece_at(chess.C1, chess.Piece(chess.BISHOP, chess.WHITE))

        # Black pawns
        for file in range(8):
            self.board.set_piece_at(chess.square(file, 6), chess.Piece(chess.PAWN, chess.BLACK))
        # Black major pieces
        self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        self.board.set_piece_at(chess.D8, chess.Piece(chess.QUEEN, chess.BLACK))
        self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
        self.board.set_piece_at(chess.B8, chess.Piece(chess.KNIGHT, chess.BLACK))
        self.board.set_piece_at(chess.C8, chess.Piece(chess.BISHOP, chess.BLACK))

    # ---------------- Main Game Loop ----------------
    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            # Draw everything
            self.screen.fill((48, 46, 43))
            self.ui.draw_board(self.board, self.selected_square, self.previous_move, self.last_move_squares, self.mode)
            self.ui.draw_pieces(self.board, use_png=True, mode=self.mode)
            self.draw_valid_moves()
            pygame.draw.rect(self.screen, (64, 64, 60), (0, 640, self.WIDTH, self.TAB_HEIGHT))
            self.draw_buttons(mouse_pos)
            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result == "MainMenu":
                        return "menu"

        return "menu"

    # ---------------- Draw Pieces ----------------
    def draw_pieces(self):
        for square, piece in self.board.piece_map().items():
            rank = chess.square_rank(square)
            if self.mode == "Half Board":
                # Map full-board ranks to compressed 4-row layout
                if rank <= 1:  # White pawns and back rank
                    row = rank
                elif rank >= 6:  # Black pawns and back rank
                    row = rank - 4
                else:
                    continue  # skip empty middle rows
            else:
                row = 7 - rank  # full-board normal

            col = chess.square_file(square)
            square_size = self.SQUARE_SIZE
            if self.mode == "Half Board":
                square_size = self.WIDTH // 8  # enlarge squares to fit horizontally
                # vertically scale to fill board
                row = int(row * self.HEIGHT / 4 / square_size)

            key = piece.symbol().upper() + ('w' if piece.color == chess.WHITE else 'b')
            img = self.pieces_images.get(key)
            if img:
                self.screen.blit(img, (col * square_size, row * square_size))

    # ---------------- Draw Buttons ----------------
    def draw_buttons(self, mouse_pos):
        for rect, text in [(self.undo_rect, "Undo"),
                           (self.draw_rect, "Draw"),
                           (self.menu_rect, "Main Menu"),
                           (self.review_rect, "Review Moves")]:
            color = (118, 150, 86)
            if rect.collidepoint(mouse_pos):
                color = (150, 180, 120)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            font = pygame.freetype.SysFont("Arial", 28)
            surf, rect_text = font.render(text, (255, 255, 255))
            rect_text.center = rect.center
            self.screen.blit(surf, rect_text)

    # ---------------- Draw Legal Moves ----------------
    def draw_valid_moves(self):
        if not self.app.settings.get("highlight_legal_moves", True):
            return

        square_size = self.SQUARE_SIZE

        if self.mode == "Half Board":
            visible_files = range(5)
            cols = len(visible_files)
            total_board_width = square_size * cols
            x_offset = (self.WIDTH - total_board_width) // 2
            y_offset = (self.HEIGHT - square_size * 8 - 60) // 2

        for move in self.valid_moves:
            row = 7 - chess.square_rank(move.to_square)
            col = chess.square_file(move.to_square)

            # Skip hidden files in half mode
            if self.mode == "Half Board" and col >= 5:
                continue

            if self.mode == "Half Board":
                file_index = list(range(5)).index(col)
                pos_x = x_offset + file_index * square_size + square_size // 2
                pos_y = y_offset + row * square_size + square_size // 2
            else:
                pos_x = col * square_size + square_size // 2
                pos_y = row * square_size + square_size // 2

            pygame.draw.circle(self.screen, (255, 0, 0), (pos_x, pos_y), 15)

    def handle_click(self, pos):
        if self.undo_rect.collidepoint(pos) and self.move_history and not self.board.is_game_over():
            self.board.pop()
            self.move_history.pop()
            self.previous_move = None
            self.last_move_squares = None
            return

        elif self.draw_rect.collidepoint(pos) and not self.board.is_game_over():
            self.show_banner("Draw agreed", (255, 165, 0), 2000)
            return

        elif self.review_rect.collidepoint(pos):
            self.review_moves()
            return

        elif self.menu_rect.collidepoint(pos):
            return "MainMenu"

        # --- Board clicks ---
        else:
            square = self.ui.get_square_from_mouse(pos, mode=self.mode)
            if square is not None:
                piece = self.board.piece_at(square)
                if self.selected_square is None:
                    if piece and piece.color == self.board.turn:
                        self.selected_square = square
                        self.valid_moves = [m for m in self.board.legal_moves if m.from_square == square]
                else:
                    move = chess.Move(self.selected_square, square)
                    moving_piece = self.board.piece_at(self.selected_square)

                    # Handle promotion
                    if moving_piece and moving_piece.piece_type == chess.PAWN:
                        if (self.board.turn and chess.square_rank(square) == 7) or \
                                (not self.board.turn and chess.square_rank(square) == 0):
                            promotion_piece = self.choose_promotion(self.board.turn)
                            move = chess.Move(self.selected_square, square, promotion=promotion_piece)

                    if move in self.board.legal_moves:
                        self.board.push(move)
                        self.move_history.append(move)
                        self.previous_move = (move.from_square, move.to_square)
                        self.last_move_squares = (move.from_square, move.to_square)

                        if self.board.is_check():
                            self.show_banner("Check!", (255, 165, 0), 2000)
                        if self.board.is_checkmate():
                            winner = "White" if self.board.turn == chess.BLACK else "Black"
                            self.show_banner(f"Checkmate! {winner} wins", (255, 50, 50), 3000)

                    self.valid_moves = []
                    self.selected_square = None
    # ---------------- Review Moves ----------------
    def review_moves(self, board_type="full"):
        """Replay all moves from the start of the game one by one.

        board_type: "full" or "half"
        """
        if not self.move_history:
            self.show_banner("No moves to review", (255, 100, 100), 2000)
            return

        # Initialize a board with the standard starting position
        review_board = chess.Board()

        for move_entry in self.move_history:
            # Convert string to chess.Move if needed
            if isinstance(move_entry, str):
                move = chess.Move.from_uci(move_entry)
            else:
                move = move_entry

            # Only push legal moves
            if move in review_board.legal_moves:
                review_board.push(move)
            else:
                print(f"Skipping illegal move: {move} on {review_board.fen()}")
                continue

            # Draw the board according to the selected type
            if board_type == "full":
                self.ui.draw_board(review_board)
                self.ui.draw_pieces(review_board)    # Full board
            elif board_type == "half":
                self.draw_half_board(review_board)  # Half board (only active side)

            pygame.display.flip()
            pygame.time.delay(500)  # Small delay to make replay visible

        import time
        review_board = chess.Board()

        # Recreate your board setup (important for half mode!)
        if self.mode == "Half Board":
            # Use same setup method as your main game
            self.setup_half_board()
            review_board = self.board.copy()
            review_board.clear_stack()
            self.setup_half_board()  # sets up self.board
            review_board = self.board.copy()  # copy the setup into review_board
            review_board.clear_stack()  # optional: clears undo history
        else:
            review_board = chess.Board()  # full board

        self.show_banner("Replaying moves...", (100, 200, 255), 1500)

        # Replay each move with short delay
        for i, move in enumerate(self.move_history):
            if isinstance(move_entry, str):
                move = chess.Move.from_uci(move_entry)
            else:
                move = move_entry

            if move in review_board.legal_moves:
                review_board.push(move)
            else:
                print(f"Skipping illegal move during replay: {move} on {review_board.fen()}")
                continue
            review_board.push(move)
            self.ui.draw_board(review_board, None, (move.from_square, move.to_square), None, self.mode)
            self.ui.draw_pieces(review_board, use_png=True, mode=self.mode)
            pygame.display.flip()
            pygame.time.wait(600)  # delay between moves (in ms)

        self.show_banner("Review complete", (100, 255, 100), 1500)
    # --------------- Promotion ----------------
    def choose_promotion(self, color):
        piece_map = {
            chess.QUEEN: QW if color == chess.WHITE else QB,
            chess.ROOK: RW if color == chess.WHITE else RB,
            chess.BISHOP: BW if color == chess.WHITE else BB,
            chess.KNIGHT: NW if color == chess.WHITE else NB
        }

        buttons = []  # list of tuples (rect, piece_type)
        if self.mode == "Half Board":
            visible_files = range(5)
            total_board_width = self.SQUARE_SIZE * len(visible_files)
            x_offset = (self.WIDTH - total_board_width) // 2
            center_x = x_offset + total_board_width // 2
        else:
            center_x = self.WIDTH // 2

        start_x = center_x - 150
        y = 300

        width, height = 80, 80
        for i, (ptype, img) in enumerate(piece_map.items()):
            rect = pygame.Rect(start_x + i * 100, y, width, height)
            buttons.append((rect, ptype))  # store as tuple

        choosing = True
        choice = chess.QUEEN
        while choosing:
            self.screen.fill((48, 46, 43))
            font = pygame.freetype.SysFont("Arial", 50)
            surf, rect_text = font.render("Choose Promotion", (255, 255, 255))
            rect_text.center = (self.WIDTH // 2, 150)
            self.screen.blit(surf, rect_text)

            mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

            for rect, ptype in buttons:
                # Check hover effect
                if rect.collidepoint(mouse_pos):
                    color = (200, 180, 120)  # Highlight color
                else:
                    color = (118, 150, 86)  # Normal color

                pygame.draw.rect(self.screen, color, rect, border_radius=10)

                # Center the piece image inside the button
                img = piece_map[ptype]
                img_scaled = pygame.transform.smoothscale(img, (rect.width - 10, rect.height - 10))
                img_rect = img_scaled.get_rect(center=rect.center)
                self.screen.blit(img_scaled, img_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, ptype in buttons:
                        if rect.collidepoint(event.pos):
                            choice = ptype
                            choosing = False

        return choice

    # ---------------- Banner ----------------
    def show_banner(self, text, color, duration=2000):
        start_time = pygame.time.get_ticks()
        banner_height = 100
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            screen_copy = self.screen.copy()
            self.screen.blit(screen_copy, (0, 0))
            banner_surf = pygame.Surface((self.WIDTH, banner_height), pygame.SRCALPHA)
            alpha = min(255, (pygame.time.get_ticks() - start_time) / duration * 255)
            banner_surf.fill((0, 0, 0, int(alpha * 0.5)))
            font = pygame.freetype.SysFont("Arial", 50)
            text_surf, text_rect = font.render(text, color)
            if self.mode == "Half Board":
                visible_files = range(5)
                total_board_width = self.SQUARE_SIZE * len(visible_files)
                x_offset = (self.WIDTH - total_board_width) // 2
                center_x = x_offset + total_board_width // 2
            else:
                center_x = self.WIDTH // 2

            text_rect.center = (center_x, banner_height // 2)
            banner_surf.blit(text_surf, text_rect)
            self.screen.blit(banner_surf, (0, self.HEIGHT // 2 - banner_height // 2))
            pygame.display.flip()
            pygame.time.wait(30)

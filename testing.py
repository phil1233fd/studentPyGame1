import sys
import pygame
import chess
import pygame.freetype
from ChessBoardUI import ChessBoardUI

# ---------------- Constants ----------------
WIDTH, HEIGHT = 640, 700
BG_COLOR = (48, 46, 43)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# ---------------- Load Piece Images ----------------
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
    Chess game session (Player vs Player)
    Supports full and half-board modes.
    """

    def __init__(self, app, mode="Full Board"):
        self.app = app
        self.screen = app.screen
        self.WIDTH, self.HEIGHT = app.screen.get_size()
        self.mode = mode

        # UI
        self.ui = ChessBoardUI(self.screen, self.WIDTH, self.HEIGHT)
        self.SQUARE_SIZE = self.ui.SQUARE_SIZE

        # Piece mapping
        self.pieces_images = {
            'Pw': PW, 'Pb': PB,
            'Rw': RW, 'Rb': RB,
            'Nw': NW, 'Nb': NB,
            'Bw': BW, 'Bb': BB,
            'Qw': QW, 'Qb': QB,
            'Kw': KW, 'Kb': KB,
        }

        # Board setup
        if mode == "Half Board":
            self.setup_half_board()
        else:
            self.board = chess.Board()

        # Buttons
        self.TAB_HEIGHT = self.HEIGHT - 640
        self.undo_rect = pygame.Rect(20, 650, 120, 40)
        self.draw_rect = pygame.Rect(160, 650, 120, 40)
        self.menu_rect = pygame.Rect(300, 650, 140, 40)
        self.review_rect = pygame.Rect(450, 650, 170, 40)

        # Game state
        self.move_history = []
        self.selected_square = None
        self.previous_move = None
        self.last_move_squares = None
        self.valid_moves = []
        self.running = True

    # ---------------- Half Board Setup ----------------
    def setup_half_board(self):
        self.board = chess.Board(None)
        # White
        for file in range(8):
            self.board.set_piece_at(chess.square(file, 1), chess.Piece(chess.PAWN, chess.WHITE))
        for square, piece in [(chess.E1, chess.KING), (chess.D1, chess.QUEEN),
                              (chess.A1, chess.ROOK), (chess.B1, chess.KNIGHT),
                              (chess.C1, chess.BISHOP)]:
            self.board.set_piece_at(square, chess.Piece(piece, chess.WHITE))
        # Black
        for file in range(8):
            self.board.set_piece_at(chess.square(file, 6), chess.Piece(chess.PAWN, chess.BLACK))
        for square, piece in [(chess.E8, chess.KING), (chess.D8, chess.QUEEN),
                              (chess.A8, chess.ROOK), (chess.B8, chess.KNIGHT),
                              (chess.C8, chess.BISHOP)]:
            self.board.set_piece_at(square, chess.Piece(piece, chess.BLACK))

    # ---------------- Main Game Loop ----------------
    def run(self):
        self.running = True
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            # Draw board
            if self.mode == "Half Board":
                self.draw_half_board(self.board)
            else:
                self.draw_board(self.board)

            # Draw buttons
            self.draw_buttons(mouse_pos)

            # Draw valid moves
            self.draw_valid_moves()

            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result == "MainMenu":
                        return "menu"

        return "menu"

    # ---------------- Draw Full Board ----------------
    def draw_board(self, board):
        colors = [(240, 217, 181), (181, 136, 99)]
        for rank in range(8):
            for file in range(8):
                rect = pygame.Rect(file*self.SQUARE_SIZE, rank*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, colors[(rank+file)%2], rect)
                square = chess.square(file, 7-rank)
                piece = board.piece_at(square)
                if piece:
                    key = piece.symbol().upper() + ('w' if piece.color==chess.WHITE else 'b')
                    img = self.pieces_images.get(key)
                    if img:
                        self.screen.blit(img, rect.topleft)

    # ---------------- Draw Half Board ----------------
    def draw_half_board(self, board):
        colors = [(240, 217, 181), (181, 136, 99)]
        # Only top 4 and bottom 2 rows
        for idx, rank in enumerate([0,1,6,7]):
            for file in range(8):
                rect = pygame.Rect(file*self.SQUARE_SIZE, idx*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, colors[(rank+file)%2], rect)
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece:
                    key = piece.symbol().upper() + ('w' if piece.color==chess.WHITE else 'b')
                    img = self.pieces_images.get(key)
                    if img:
                        self.screen.blit(img, rect.topleft)

    # ---------------- Draw Buttons ----------------
    def draw_buttons(self, mouse_pos):
        for rect, text in [(self.undo_rect,"Undo"),(self.draw_rect,"Draw"),
                           (self.menu_rect,"Main Menu"),(self.review_rect,"Review Moves")]:
            color = (118,150,86)
            if rect.collidepoint(mouse_pos):
                color = (150,180,120)
            pygame.draw.rect(self.screen,color,rect,border_radius=10)
            font = pygame.freetype.SysFont("Arial",28)
            surf, rect_text = font.render(text,(255,255,255))
            rect_text.center = rect.center
            self.screen.blit(surf,rect_text)

    # ---------------- Draw Legal Moves ----------------
    def draw_valid_moves(self):
        square_size = self.SQUARE_SIZE
        for move in self.valid_moves:
            row = 7 - chess.square_rank(move.to_square)
            col = chess.square_file(move.to_square)
            pos_x = col*square_size + square_size//2
            pos_y = row*square_size + square_size//2
            pygame.draw.circle(self.screen,(255,0,0),(pos_x,pos_y),15)

    # ---------------- Handle Clicks ----------------
    def handle_click(self,pos):
        if self.undo_rect.collidepoint(pos) and self.move_history:
            self.board.pop()
            self.move_history.pop()
            self.selected_square = None
            self.valid_moves = []
            return
        elif self.draw_rect.collidepoint(pos):
            self.show_banner("Draw agreed",(255,165,0),2000)
            return
        elif self.menu_rect.collidepoint(pos):
            return "MainMenu"
        elif self.review_rect.collidepoint(pos):
            self.review_moves()
            return

        # Board clicks
        square = self.ui.get_square_from_mouse(pos, mode=self.mode)
        if square is None:
            return

        piece = self.board.piece_at(square)
        if self.selected_square is None:
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.valid_moves = [m for m in self.board.legal_moves if m.from_square==square]
        else:
            move = chess.Move(self.selected_square, square)
            moving_piece = self.board.piece_at(self.selected_square)

            # Promotion
            if moving_piece and moving_piece.piece_type==chess.PAWN:
                rank = chess.square_rank(square)
                if (moving_piece.color==chess.WHITE and rank==7) or (moving_piece.color==chess.BLACK and rank==0):
                    move = chess.Move(self.selected_square,square,promotion=self.choose_promotion(moving_piece.color))

            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move)
                self.previous_move = (move.from_square, move.to_square)
                self.last_move_squares = (move.from_square, move.to_square)
                if self.board.is_check():
                    self.show_banner("Check!",(255,165,0),2000)
                if self.board.is_checkmate():
                    winner = "White" if self.board.turn==chess.BLACK else "Black"
                    self.show_banner(f"Checkmate! {winner} wins",(255,50,50),3000)

            self.selected_square=None
            self.valid_moves=[]

    # ---------------- Promotion ----------------
    def choose_promotion(self,color):
        return chess.QUEEN  # default promotion (simpler, can add GUI later)

    # ---------------- Review Moves ----------------
    def review_moves(self):
        if not self.move_history:
            self.show_banner("No moves to review",(255,100,100),2000)
            return
        review_board = chess.Board()
        for move in self.move_history:
            if isinstance(move,str):
                move = chess.Move.from_uci(move)
            if move in review_board.legal_moves:
                review_board.push(move)
            self.screen.fill(BG_COLOR)
            if self.mode=="Half Board":
                self.draw_half_board(review_board)
            else:
                self.draw_board(review_board)
            pygame.display.flip()
            pygame.time.wait(500)
        self.show_banner("Review complete",(100,255,100),1500)

    # ---------------- Banner ----------------
    def show_banner(self,text,color,duration=2000):
        start_time = pygame.time.get_ticks()
        banner_height = 100
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
            banner_surf = pygame.Surface((self.WIDTH,banner_height),pygame.SRCALPHA)
            alpha = min(255,(pygame.time.get_ticks()-start_time)/duration*255)
            banner_surf.fill((0,0,0,int(alpha*0.5)))
            font = pygame.freetype.SysFont("Arial",50)
            text_surf,text_rect = font.render(text,color)
            text_rect.center=(self.WIDTH//2,banner_height//2)
            banner_surf.blit(text_surf,text_rect)
            self.screen.blit(banner_surf,(0,self.HEIGHT//2 - banner_height//2))
            pygame.display.flip()
            pygame.time.wait(30)

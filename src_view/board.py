import tkinter as tk
from PIL import Image, ImageTk

from src.Models.chess_board import ChessBoard
from src.Models.chess_square import ChessSquare
from src.Models.piece import Piece

white_square = "#18D9AC"
black_square = "#BED8D2"
highlight_square = "#91C73B"


def set_color(position_x: int, position_y: int) -> str:
    return white_square if (position_x + position_y) % 2 == 0 else black_square


class SquareCanvas(tk.Canvas):
    def __init__(self, master, chess_square: ChessSquare, click_callback):
        super().__init__(master, width=100, height=100, background=set_color(chess_square.x, chess_square.y))
        # Variables
        self.is_highlighted = False

        self.chess_square = chess_square
        self.position_x = chess_square.x
        self.position_y = chess_square.y
        self.click_callback = click_callback
        if chess_square.has_value:
            self.display_piece(chess_square.piece)
        # Add coordinates text
        self.create_text(50, 10, text=f'{self.position_x},{self.position_y}', fill='black')
        # Listen click
        self.bind("<Button-1>", self.on_square_clicked)

    def display_piece(self, piece: Piece):
        image = Image.open(piece.path)
        image = image.resize((70, 70), Image.Resampling.LANCZOS)
        self.piece_image = ImageTk.PhotoImage(image)
        self.create_image(50, 50, image=self.piece_image)

    def on_square_clicked(self, event):
        self.click_callback(self)
        print(self.is_highlighted)


class BoardCanvas(tk.Canvas):
    def __init__(self, master, h, w, click_callback):
        super().__init__(master)
        self.configure(width=w, height=h)
        self.grid(row=0, column=0)
        self.click_callback = click_callback

    def add_square(self, chess_square: ChessSquare, click_callback):
        square = SquareCanvas(self, chess_square, click_callback)
        square.grid(row=chess_square.y, column=chess_square.x)


class BoardWindow(tk.Tk):
    def __init__(self, chess_board: ChessBoard):
        super().__init__()

        # Variables
        self.possible_moves_list = None

        # Move variables
        self.new_position = None
        self.last_selected_piece = None

        self.title("Chess Board")
        self.board = BoardCanvas(self, 800, 800, self.handle_square_click)
        self.create_board(chess_board)

    def create_board(self, board: ChessBoard):
        for i in range(8):
            for j in range(8):
                self.board.add_square(board.board[i][j], self.handle_square_click)

    def highlight_squares(self, squares: list):
        pass

    def handle_square_click(self, square_canvas):
        if self.last_selected_piece and self.last_selected_piece is not square_canvas:
            # Unselect the last square
            self.last_selected_piece.is_highlighted = False
            self.last_selected_piece.config(
                background=set_color(self.last_selected_piece.position_x, self.last_selected_piece.position_y))

        # Select the new
        if square_canvas.chess_square.has_value:
            square_canvas.config(background=highlight_square)
            self.last_selected_piece = square_canvas
            self.last_selected_piece.is_highlighted = True

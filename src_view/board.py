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
    def __init__(self, master, chess_square: ChessSquare):
        super().__init__(master, width=100, height=100, background=set_color(chess_square.x, chess_square.y))
        self.position_x = chess_square.x
        self.position_y = chess_square.y
        if chess_square.has_value:
            self.display_piece(chess_square.piece)

        self.create_text(80, 10, text=f'{self.position_x},{self.position_y}', fill='black')

    def display_piece(self, piece: Piece):
        image = Image.open(piece.path)
        image = image.resize((80, 80), Image.Resampling.LANCZOS)
        self.piece_image = ImageTk.PhotoImage(image)
        self.create_image(50, 50, image=self.piece_image)


class BoardCanvas(tk.Canvas):
    def __init__(self, master, h, w):
        super().__init__(master)
        self.configure(width=w, height=h)
        self.grid(row=0, column=0)

    def add_square(self, chess_square: ChessSquare):
        square = SquareCanvas(self, chess_square)
        square.grid(row=chess_square.y, column=chess_square.x)


class BoardWindow(tk.Tk):
    def __init__(self, chess_board: ChessBoard):
        super().__init__()
        self.title("Chess Board")
        self.board = BoardCanvas(self, 800, 800)
        self.create_board(chess_board)

    def create_board(self, board: ChessBoard):
        for i in range(8):
            for j in range(8):
                self.board.add_square(board.board[i][j])

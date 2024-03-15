import tkinter as tk
import numpy as np

from src.Models.chess_square import ChessSquare
from src.Models.chess_board import ChessBoard


class SquareCanvas(tk.Canvas):
    def __init__(self, master, chess_square: ChessSquare):
        super().__init__(master, width=100, height=100, background=self.set_color(chess_square.x, chess_square.y))
        self.position_x = chess_square.x
        self.position_y = chess_square.y

    def set_color(self, position_x: int, position_y: int) -> str:
        if (position_x + position_y) % 2 == 0:
            return "white"
        else:
            return "black"


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
        self.board = BoardCanvas(self, 1000, 1000)
        self.create_board(chess_board)

    def create_board(self, chess_board: ChessBoard):
        for i in range(8):
            for j in range(8):
                self.board.add_square(chess_board.board[i][j])


if __name__ == "__main__":
    chess_board = ChessBoard()
    app = BoardWindow(chess_board)
    app.mainloop()

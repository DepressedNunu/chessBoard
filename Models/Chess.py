import tkinter as tk
import numpy
from Models.piece import *


class ChessSquare(tk.Canvas):
    def __init__(self, master, color, piece=None, **kwargs):
        super().__init__(master, width=100, height=93, bg=color, **kwargs)
        self.piece = piece

        if self.piece:
            self.add_piece()

    def add_piece(self):
        color = "BLACK" if self.piece < 0 else "WHITE"
        piece_type = abs(self.piece)
        image_path = f"images/{color}/{color.lower()}_{'pawn' if piece_type == 1 else 'king' if piece_type == 6 else 'queen' if piece_type == 5 else 'bishop' if piece_type == 3 else 'horse' if piece_type == 4 else 'tower'}.png"
        self.image = tk.PhotoImage(file=image_path)
        self.create_image(50, 50, image=self.image)


class ChessBoard(tk.Frame):
    chessData = numpy.array([[0 for i in range(8)] for j in range(8)])

    def place_piece(self, piece: Piece):
        self.chessData[piece.position[1]][piece.position[0]] = piece.pieceType.value
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.create_board()

    def move_piece(self, piece: Piece, new_position: tuple):
        if self.validate_move(piece, new_position):
            self.chessData[piece.position[1]][piece.position[0]] = 0
            piece.move(new_position)
            self.chessData[new_position[1]][new_position[0]] = piece.pieceType.value

    def validate_move(self, piece: Piece, new_position: tuple):
        return True

    def display_board(self):
        for row in self.chessData:
            print(row)
    def create_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                piece = self.chessboard[j][i]
                square = ChessSquare(self.root, color, piece, highlightthickness=0)
                square.grid(row=j, column=i, padx=1, pady=1)

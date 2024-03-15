import tkinter as tk
import numpy
from src.Models.piece import *


class ChessBoard(tk.Frame):
    chessData = numpy.array([[0 for i in range(8)] for j in range(8)])

    def place_piece(self, piece: Piece):
        self.chessData[piece.position[1]][piece.position[0]] = piece.pieceType.value

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

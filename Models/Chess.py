import tkinter as tk
import numpy
from Models.piece import *


class ChessBoard(tk.Frame):
    chessData = numpy.array([[0 for i in range(8)] for j in range(8)])
    Map_positions = {}  # Dictionary to map positions to pieces

    def place_piece(self, piece: Piece):
        x, y = piece.position
        self.chessData[y][x] = piece.pieceType.value  # type the right number in the chessBoard
        self.Map_positions[(x, y)] = piece  # map the new position of the piece to the Dictionnary
        self.chessData[piece.position[1]][piece.position[0]] = piece.pieceType.value

    def move_piece(self, piece: Piece, new_position: tuple):
        if self.validate_move(piece, new_position):  # if the move is valid
            x, y = piece.position
            self.chessData[y][x] = 0  # Delete the old position of the Piece
            del self.Map_positions[(x, y)]  # Delete the old position in the Dictionnary
            self.chessData[piece.position[1]][piece.position[0]] = 0

            # Once the Piece has moved, changed his positions data
            piece.move(new_position)
            x, y = new_position
            self.chessData[y][x] = piece.pieceType.value
            self.Map_positions[(x, y)] = piece

    def get_piece_position_list(self):
        return self.Map_positions

    def get_piece_at_position(self, position: tuple):
        return self.Map_positions.get(position, None)

    def validate_move(self, piece: Piece, new_position: tuple):
        return True

    def display_board(self):
        for row in self.chessData:
            print(row)

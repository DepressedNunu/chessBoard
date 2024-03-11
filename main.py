from Models import *
import tkinter as tk

from Models.Chess import ChessBoard
from Models.piece import Piece
from Models.piece import PieceType

if __name__ == '__main__':
    board = ChessBoard()
    board.display_board()
    print("\n===========================================\n")

    board.display_board()
    currentPiece = board.get_piece_at_position((0, 1))
    board.move_piece(currentPiece, (0, 3))
    print("\n===========================================\n")

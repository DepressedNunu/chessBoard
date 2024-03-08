from Models import *
import tkinter as tk

from Models.Chess import ChessBoard
from Models.piece import Piece
from Models.piece import PieceType

if __name__ == '__main__':
    board = ChessBoard()
    board.display_board()
    print("\n===========================================\n")
    pawn = Piece(PieceType.pawnBlack, (1, 1))
    print(pawn.pieceType.value)
    print(pawn.path)
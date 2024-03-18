from Models import *
import tkinter as tk
import keyboard
from Models.Chess import ChessBoard
from Models.piece import Piece
from Models.piece import PieceType

if __name__ == "__main__":
    chess_board = ChessBoard()
    app = BoardWindow(chess_board)
    app.mainloop()

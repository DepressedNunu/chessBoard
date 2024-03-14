from Models import *
import tkinter as tk
import keyboard
from Models.Chess import ChessBoard
from Models.piece import Piece
from Models.piece import PieceType

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chess")
    board = ChessBoard()
    board.draw_board(root)

    # WRITING DATA TO THE BOARD

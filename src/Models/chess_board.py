import numpy as np

from src.Models.chess_square import ChessSquare


class ChessBoard:
    def __init__(self):
        board_list = [[ChessSquare(i, j) for j in range(8)] for i in range(8)]
        self.board = np.array(board_list, dtype=object)

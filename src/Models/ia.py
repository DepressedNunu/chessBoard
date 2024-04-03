import random

from src.Models.moves import Move
from src.Models.piece import Position


class ia:
    def __init__(self, board):
        self.board = board

    def play(self, board, piece_list):
        piece, destination = self.get_move(board, piece_list)
        self.board.move(piece, destination[::-1])
        return piece, destination

    def get_move(self, board, piece_list):
        # without CSV
        piece, move = self.get_random_value(board, piece_list)
        return piece, move

    @staticmethod
    def get_random_value(board, piece_list):
        move = None
        piece = None
        list_move = None
        while move is None or list_move is None:
            piece = random.choice(piece_list)
            list_move = board.filter_possible_moves(piece)
            if len(list_move) == 0 or list_move is None:
                continue
            move = list_move[0]
            move = (move[1], move[0])

        return piece, move

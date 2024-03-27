import random


class ia:
    def __init__(self, board):
        self.board = board

    def play(self, board, piece_list):
        piece, move = self.get_move(board, piece_list)
        print(f"IA move: {piece.pieceType} to {move}")
        self.board.move(piece, move[::-1])

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
            list_move = board.get_possible_moves(piece)
            if list_move is [] or list_move is None:
                piece = None
                continue
            move = list_move[0]
            move = (move[1], move[0])

        return piece, move

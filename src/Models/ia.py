import csv
import random

from src.Models.moves import Move
from src.Models.piece import Position

from src.Models.moves import Move

class ia:
    def __init__(self, board):
        self.board = board

    def play(self, board):
        piece, destination = self.get_move(board)

        move = Move(
            initial_position=Position(piece.position.x, piece.position.y),
            move_position=Position(destination[0], destination[1]),
            piece=piece,
            captured_piece=board.board[destination[1]][destination[0]].piece)

        self.board.move(piece, destination[::-1])
        board.game_moves.add_move(move, board.is_check(board.turn),
                                  board.is_checkmate(board.turn))

    def get_move(self, board):
        # iterate through all the board, and retrieve all the pieces
        test_list = []

        for i in range(8):
            for j in range(8):
                piece = board.board[i][j].piece
                if piece is not None and piece.color == board.turn:
                    test_list.append(piece)

        # with CSV
        piece, move = self.get_random_value(board, test_list)

        # with CSV
        #piece, move = self.get_best_value(board, test_list)

        return piece, move

    def sort_moves_by_winrate(self):
        moves_count = {}
        wins_count = {}
        with open('saves/games_saves.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row['Moves'] == 'Turns' or row['Moves'].startswith('('):
                    continue
                move = row['White'] if row['White'] else row['Black']
                white_win_score = float(row['White_move_score']) if row['White_move_score'] else 0
                black_win_score = float(row['Black_move_score']) if row['Black_move_score'] else 0
                if move in moves_count:
                    moves_count[move] += 1
                else:
                    moves_count[move] = 1
                if white_win_score > 0 or black_win_score > 0:
                    if move in wins_count:
                        wins_count[move] += 1
                    else:
                        wins_count[move] = 1
        moves_winrates = {}
        for move, count in moves_count.items():
            win_count = wins_count.get(move, 0)
            win_rate = win_count / count
            moves_winrates[move] = win_rate
        sorted_moves = sorted(moves_winrates.items(), key=lambda x: x[1], reverse=True)
        return sorted_moves

    def get_best_value(self, board, piece_list):
        sorted_moves = self.sort_moves_by_winrate()
        for move, _ in sorted_moves:
            for piece in piece_list:
                possible_moves = board.filter_possible_moves(piece)
                if move in possible_moves:
                    return piece, move
        # If no move with a win rate is found, return a random move
        return self.get_random_value(board, piece_list)

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
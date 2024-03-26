import random

import numpy as np

from src.Models.chess_square import ChessSquare
from src.Models.piece import Piece, PieceType, Position
from src_view.board import SquareCanvas

pieces_list = [
    # test purposes
    Piece(PieceType.BISHOP_BLACK, Position(5, 3), False),

    Piece(PieceType.ROOK_BLACK, Position(0, 0), False),
    Piece(PieceType.KNIGHT_BLACK, Position(0, 1), False),
    Piece(PieceType.BISHOP_BLACK, Position(0, 2), False),
    Piece(PieceType.QUEEN_BLACK, Position(0, 3), False),
    Piece(PieceType.KING_BLACK, Position(0, 4), False),
    Piece(PieceType.BISHOP_BLACK, Position(5, 3), False),
    Piece(PieceType.KNIGHT_BLACK, Position(0, 6), False),
    Piece(PieceType.ROOK_BLACK, Position(0, 7), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 0), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 1), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 2), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 3), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 4), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 5), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 6), False),
    Piece(PieceType.PAWN_BLACK, Position(1, 7), False),
    Piece(PieceType.PAWN_WHITE, Position(6, 0), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 1), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 2), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 3), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 4), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 5), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 6), True),
    Piece(PieceType.PAWN_WHITE, Position(6, 7), True),
    Piece(PieceType.ROOK_WHITE, Position(7, 0), True),
    Piece(PieceType.KNIGHT_WHITE, Position(7, 1), True),
    Piece(PieceType.BISHOP_WHITE, Position(7, 2), True),
    Piece(PieceType.QUEEN_WHITE, Position(7, 3), True),
    Piece(PieceType.KING_WHITE, Position(7, 4), True),
    Piece(PieceType.BISHOP_WHITE, Position(7, 5), True),
    Piece(PieceType.KNIGHT_WHITE, Position(7, 6), True),
    Piece(PieceType.ROOK_WHITE, Position(7, 7), True),
]

class ChessBoard:
    def __init__(self):
        self.possible_moves_list = []
        self.possible_kings_list = [pieces_list[28]]

        self.board = np.array([[ChessSquare(i, j) for i in range(8)] for j in range(8)], dtype=object)

        self.setup_pieces()
        self.last_selected_piece = None
        self.turn = random.randint(0, 1) == 0

    def setup_pieces(self):
        for piece in pieces_list:
            x, y = piece.position.x, piece.position.y
            square = self.board[x][y]
            square.piece = piece
            square.has_value = True

    def get_linear_moves(self, piece, directions):
        """
        Helper function to calculate possible moves for pieces that move in straight lines (rooks and queens).
        """
        row, col = piece.position.x, piece.position.y
        possible_moves = []
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col):
                        possible_moves.append((new_row, new_col))
                    elif self.is_ennemy_piece(new_row, new_col, piece.color):
                        possible_moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return possible_moves

    def get_diagonal_moves(self, piece, directions):
        """
        Helper function to calculate possible moves for pieces that move diagonally (bishops and queens).
        """
        row, col = piece.position.x, piece.position.y
        possible_moves = []
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col):
                        possible_moves.append((new_row, new_col))
                    elif self.is_ennemy_piece(new_row, new_col, piece.color):
                        possible_moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return possible_moves

    def is_empty_square(self, row, col):
        return self.is_valid_position(row, col) and self.board[row][col].piece is None

    def is_ennemy_piece(self, row, col, color):
        return self.is_valid_position(row, col) and self.board[row][col].piece is not None and \
            self.board[row][col].piece.color != color

    @staticmethod
    def is_valid_position(row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def pawn_possible_moves(self, piece: Piece):
        print(piece)
        row, col = piece.position.x, piece.position.y
        self.possible_moves_list = []
        pawn_direction = -1 if piece.color else 1

        # Single square move
        if self.is_empty_square(row + pawn_direction, col):
            self.possible_moves_list.append((row + pawn_direction, col))
            # Double square move for pawns in their initial position
            if (row == 1 and not piece.color) or (row == 6 and piece.color):
                if self.is_empty_square(row + 2 * pawn_direction, col):
                    self.possible_moves_list.append((row + 2 * pawn_direction, col))

        # Capture moves
        for dcol in [-1, 1]:
            new_row, new_col = row + pawn_direction, col + dcol
            if self.is_valid_position(new_row, new_col) and self.is_ennemy_piece(new_row, new_col, piece.color):
                self.possible_moves_list.append((new_row, new_col))
        return self.possible_moves_list

    def rook_possible_moves(self, piece: Piece):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self.get_linear_moves(piece, directions)

    def bishop_possible_moves(self, piece: Piece):
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        return self.get_diagonal_moves(piece, directions)

    def queen_possible_moves(self, piece: Piece):
        # Combine rook and bishop movements
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        return self.get_linear_moves(piece, directions) + self.get_diagonal_moves(piece, directions)

    def knight_possible_moves(self, piece: Piece):
        row, col = piece.position.x, piece.position.y
        possible_moves = []
        for drow, dcol in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
            new_row, new_col = row + drow, col + dcol
            if self.is_valid_position(new_row, new_col):
                if self.is_empty_square(new_row, new_col) or self.is_ennemy_piece(new_row, new_col, piece.color):
                    possible_moves.append((new_row, new_col))
        return possible_moves

    def king_possible_moves(self, piece: Piece):
        row, col = piece.position.x, piece.position.y
        possible_moves = []
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                new_row, new_col = row + drow, col + dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col) or self.is_ennemy_piece(new_row, new_col, piece.color):
                        possible_moves.append((new_row, new_col))

        self.check_(piece, possible_moves)
        return possible_moves

    def move(self, piece: Piece, new_position: tuple):
        old_row, old_col = piece.position.x, piece.position.y
        new_row, new_col = new_position[1], new_position[0]

        print(f"Moving piece {piece.pieceType} from ({old_row}, {old_col}) to ({new_row}, {new_col})")
        move_to_algebraic_notation = chr(ord('a') + new_col) + str(8 - new_row)
        piece.position.x, piece.position.y = new_row, new_col

        self.board[new_row][new_col].piece = piece
        self.board[new_row][new_col].has_value = True
        self.board[old_row][old_col].piece = None
        self.board[old_row][old_col].has_value = False

        self.last_selected_piece = None
        self.possible_moves_list = None

    def get_possible_moves(self, piece: Piece):
        if piece.pieceType == PieceType.KING_BLACK or piece.pieceType == PieceType.KING_WHITE:
            self.king_possible_moves(piece)
        if piece.pieceType == PieceType.ROOK_BLACK or piece.pieceType == PieceType.ROOK_WHITE:
            self.rook_possible_moves(piece)
        if piece.pieceType == PieceType.PAWN_BLACK or piece.pieceType == PieceType.PAWN_WHITE:
            self.pawn_possible_moves(piece)
        if piece.pieceType == PieceType.BISHOP_BLACK or piece.pieceType == PieceType.BISHOP_WHITE:
            self.bishop_possible_moves(piece)
        if piece.pieceType == PieceType.KNIGHT_BLACK or piece.pieceType == PieceType.KNIGHT_WHITE:
            self.knight_possible_moves(piece)
        if piece.pieceType == PieceType.QUEEN_BLACK or piece.pieceType == PieceType.QUEEN_WHITE:
            self.queen_possible_moves(piece)

        return self.possible_moves_list

    def check_(self, piece: Piece, king_possibles_moves):
        adversary_possible_moves = []
        for pos_x, pos_y in king_possibles_moves:
            possible_king = Piece(PieceType.KING_WHITE, Position(pos_x, pos_y), True)
            pieces_list.append(possible_king)

        for adversary_piece in pieces_list:
            if adversary_piece.color != piece.color and adversary_piece.pieceType != PieceType.KING_BLACK:
                p = self.get_possible_moves(adversary_piece)
                print("adversary_possible_moves for ", adversary_piece.pieceType)
                print(self.get_possible_moves(adversary_piece))
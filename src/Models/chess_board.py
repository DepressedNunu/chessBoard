import random

import numpy as np

from src.Models.chess_square import ChessSquare
from src.Models.moves import GameMoves
from src.Models.piece import Piece, PieceType, Position
from src_view import board
from src_view.board import SquareCanvas

pieces_list = [
    Piece(PieceType.BISHOP, Position(0, 5), False),
    Piece(PieceType.ROOK, Position(0, 0), False),
    Piece(PieceType.KNIGHT, Position(0, 1), False),
    Piece(PieceType.BISHOP, Position(0, 2), False),
    Piece(PieceType.QUEEN, Position(0, 3), False),
    Piece(PieceType.KING, Position(0, 4), False),
    Piece(PieceType.KNIGHT, Position(0, 6), False),
    Piece(PieceType.ROOK, Position(0, 7), False),
    Piece(PieceType.PAWN, Position(1, 0), False),
    Piece(PieceType.PAWN, Position(1, 1), False),
    Piece(PieceType.PAWN, Position(1, 2), False),
    Piece(PieceType.PAWN, Position(1, 3), False),
    Piece(PieceType.PAWN, Position(1, 4), False),
    Piece(PieceType.PAWN, Position(1, 5), False),
    Piece(PieceType.PAWN, Position(1, 6), False),
    Piece(PieceType.PAWN, Position(1, 7), False),
    Piece(PieceType.PAWN, Position(6, 0), True),
    Piece(PieceType.PAWN, Position(6, 1), True),
    Piece(PieceType.PAWN, Position(6, 2), True),
    Piece(PieceType.PAWN, Position(6, 3), True),
    Piece(PieceType.PAWN, Position(6, 4), True),
    Piece(PieceType.PAWN, Position(6, 5), True),
    Piece(PieceType.PAWN, Position(6, 6), True),
    Piece(PieceType.PAWN, Position(6, 7), True),
    Piece(PieceType.ROOK, Position(7, 0), True),
    Piece(PieceType.KNIGHT, Position(7, 1), True),
    Piece(PieceType.BISHOP, Position(7, 2), True),
    Piece(PieceType.QUEEN, Position(7, 3), True),
    Piece(PieceType.KING, Position(7, 4), True),
    Piece(PieceType.BISHOP, Position(7, 5), True),
    Piece(PieceType.KNIGHT, Position(7, 6), True),
    Piece(PieceType.ROOK, Position(7, 7), True),
]


class ChessBoard:
    def __init__(self):
        self.enemy_piece_moves = []
        self.possible_moves_list = []
        self.possible_kings_list = [pieces_list[28]]

        self.board = np.array([[ChessSquare(i, j) for i in range(8)] for j in range(8)], dtype=object)
        self.setup_pieces()
        self.last_selected_piece = None
        self.turn = 1

        self.game_moves = GameMoves()

    def setup_pieces(self):
        for piece in pieces_list:
            x, y = piece.position.x, piece.position.y
            square = self.board[x][y]
            square.piece = piece
            square.has_value = True

    def get_linear_moves(self, piece, directions):
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
        return possible_moves

    def move(self, piece: Piece, new_position: tuple):
        fake_piece_list = pieces_list.copy()

        old_row, old_col = piece.position.x, piece.position.y
        new_row, new_col = new_position[0], new_position[1]

        piece.position.x, piece.position.y = new_row, new_col

        # if a piece was taken, remove it from the list
        if self.board[new_row][new_col].piece is not None:
            fake_piece_list.remove(self.board[new_row][new_col].piece)
            self.board[new_row][new_col].piece = None
            self.board[new_row][new_col].has_value = False

        self.board[new_row][new_col].piece = piece
        self.board[new_row][new_col].has_value = True
        self.board[old_row][old_col].piece = None
        self.board[old_row][old_col].has_value = False

        return fake_piece_list

    def get_possible_moves(self, piece: Piece):
        if piece.pieceType == PieceType.KING:
            return self.king_possible_moves(piece)
        if piece.pieceType == PieceType.ROOK:
            return self.rook_possible_moves(piece)
        if piece.pieceType == PieceType.PAWN:
            return self.pawn_possible_moves(piece)
        if piece.pieceType == PieceType.BISHOP:
            return self.bishop_possible_moves(piece)
        if piece.pieceType == PieceType.KNIGHT:
            return self.knight_possible_moves(piece)
        if piece.pieceType == PieceType.QUEEN:
            return self.queen_possible_moves(piece)

    @staticmethod
    def get_king(color):
        for piece in pieces_list:
            if piece.pieceType == PieceType.KING:
                if piece.color == color:
                    return piece

    def is_check(self, color, copy_piece_list=None):
        if copy_piece_list is None:
            copy_piece_list = pieces_list

        king = self.get_king(color)
        king_position = king.position.x, king.position.y
        for piece in copy_piece_list:
            if piece.color != color:
                possible_moves = self.get_possible_moves(piece)
                if king_position in possible_moves:
                    return True
        return False

    def is_checkmate(self, color):
        for piece in pieces_list:
            if piece.color == color: # if the piece is not the same color as the king
                if self.filter_possible_moves(piece):
                    return False
        return True

    @staticmethod
    def get_pieces(color):
        color_pieces = []
        for piece in pieces_list:
            if piece.color == color:
                color_pieces.append(piece)
        return color_pieces

    def copy(self):  # Make a deep copy of the board
        new_board = ChessBoard()
        for i in range(8):
            for j in range(8):
                new_board.board[i][j].piece = self.board[i][j].piece
                new_board.board[i][j].has_value = self.board[i][j].has_value
        return new_board

    def filter_possible_moves(self, piece):
        possible_moves = self.get_possible_moves(piece)
        filtered_moves = []
        old_position = piece.position.x, piece.position.y
        new_board = self.copy()
        for move in possible_moves:
            fake_piece_list = new_board.move(piece, move)
            if not new_board.is_check(piece.color, fake_piece_list):
                filtered_moves.append(move)
            new_board.move(piece, (old_position[0], old_position[1]))
        self.possible_moves_list = filtered_moves
        return filtered_moves

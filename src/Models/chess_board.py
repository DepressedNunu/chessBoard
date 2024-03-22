import random

import numpy as np

from src.Models.chess_square import ChessSquare
from src.Models.piece import Piece, PieceType, Position
from src_view.board import SquareCanvas

starting_pieces_list = [
    Piece(PieceType.ROOK_BLACK, Position(0, 0)),
    Piece(PieceType.KNIGHT_BLACK, Position(0, 1)),
    Piece(PieceType.BISHOP_BLACK, Position(0, 2)),
    Piece(PieceType.QUEEN_BLACK, Position(0, 3)),
    Piece(PieceType.KING_BLACK, Position(0, 4)),
    Piece(PieceType.BISHOP_BLACK, Position(0, 5)),
    Piece(PieceType.KNIGHT_BLACK, Position(0, 6)),
    Piece(PieceType.ROOK_BLACK, Position(0, 7)),
    Piece(PieceType.PAWN_BLACK, Position(1, 0)),
    Piece(PieceType.PAWN_BLACK, Position(1, 1)),
    Piece(PieceType.PAWN_BLACK, Position(1, 2)),
    Piece(PieceType.PAWN_BLACK, Position(1, 3)),
    Piece(PieceType.PAWN_BLACK, Position(1, 4)),
    Piece(PieceType.PAWN_BLACK, Position(1, 5)),
    Piece(PieceType.PAWN_BLACK, Position(1, 6)),
    Piece(PieceType.PAWN_BLACK, Position(1, 7)),
    Piece(PieceType.PAWN_WHITE, Position(6, 0)),
    Piece(PieceType.PAWN_WHITE, Position(6, 1)),
    Piece(PieceType.PAWN_WHITE, Position(6, 2)),
    Piece(PieceType.PAWN_WHITE, Position(6, 3)),
    Piece(PieceType.PAWN_WHITE, Position(6, 4)),
    Piece(PieceType.PAWN_WHITE, Position(6, 5)),
    Piece(PieceType.PAWN_WHITE, Position(6, 6)),
    Piece(PieceType.PAWN_WHITE, Position(6, 7)),
    Piece(PieceType.ROOK_WHITE, Position(7, 0)),
    Piece(PieceType.KNIGHT_WHITE, Position(7, 1)),
    Piece(PieceType.BISHOP_WHITE, Position(7, 2)),
    Piece(PieceType.QUEEN_WHITE, Position(7, 3)),
    Piece(PieceType.KING_WHITE, Position(7, 4)),
    Piece(PieceType.BISHOP_WHITE, Position(7, 5)),
    Piece(PieceType.KNIGHT_WHITE, Position(7, 6)),
    Piece(PieceType.ROOK_WHITE, Position(7, 7)),

    # test purposes
    #Piece(PieceType.PAWN_BLACK, Position(5, 3))
]


class ChessBoard:
    def __init__(self):
        self.possible_moves_list = []
        self.board = np.array([[ChessSquare(i, j) for i in range(8)] for j in range(8)], dtype=object)
        self.setup_pieces()
        self.last_selected_piece = None
        # self.turn = random.randint(0, 1) == 0 and 'white' or 'black'
        # print(f"Turn: {self.turn}")

    def setup_pieces(self):
        for piece in starting_pieces_list:
            x, y = piece.position.x, piece.position.y
            square = self.board[x][y]
            square.piece = piece
            square.has_value = True

    def get_linear_moves(self, piece, directions) -> []:
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
        pawn_direction = 1 if piece.color == 'white' else -1

        # Single square move
        if self.is_empty_square(row + pawn_direction, col):
            self.possible_moves_list.append((row + pawn_direction, col))
            # Double square move for pawns in their initial position
            if (row == 1 and piece.color == 'white') or (row == 6 and piece.color == 'black'):
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

        possibles_moves = self.get_linear_moves(piece, directions)

        if self.castling(piece) is not None:
            possibles_moves.append((piece.position.x, 4))

        return possibles_moves  # , special_move) if special_move is not None else possibles_moves

    def castling(self, piece: Piece):
        rook_is_default = False
        king_is_default = False
        is_little_castle = True
        is_big_castle = True

        if piece.position.x in [0, 7] and piece.position.y in [0, 7]:
            rook_is_default = True

        if (self.board[0][4].piece.pieceType == PieceType.KING_BLACK or self.board[7][4]
                .piece.pieceType == PieceType.KING_WHITE):
            king_is_default = True

        little_castle = self.board[piece.position.x, 5:7]
        big_castle = self.board[piece.position.x, 1:4]

        for square in little_castle:
            if square.has_value:
                is_little_castle = False

        for square in big_castle:
            if square.has_value:
                is_big_castle = False

        if rook_is_default and king_is_default and is_big_castle:
            return "big_castle"
        elif rook_is_default and king_is_default and is_little_castle:
            return "little_castle"
        else:
            return None

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

    def get_possible_moves(self, selected_square: SquareCanvas):
        return self.possible_moves_list

    def handle_castle_move(self, piece: Piece, castle_type: bool):
        if castle_type:
            new_row, new_col = piece.position.x, 3
            new_coll_king = 2
        else:
            new_row, new_col = piece.position.x, 5
            new_coll_king = 6
        old_row, old_col = piece.position.x, piece.position.y

        piece.position.x, piece.position.y = new_row, new_col

        # move tower
        self.board[new_row][new_col].piece = piece
        self.board[new_row][new_col].has_value = True
        self.board[old_row][old_col].piece = None
        self.board[old_row][old_col].has_value = False

        # move king
        self.board[new_row][new_coll_king].piece = self.board[piece.position.x][4].piece
        self.board[new_row][new_coll_king].has_value = True
        self.board[old_row][4].piece = None
        self.board[old_row][4].has_value = False

        self.last_selected_piece = None
        self.possible_moves_list = None

    def move(self, piece: Piece, new_position: tuple):
        special_move = self.castling(piece)

        if special_move is not None:
            self.handle_castle_move(piece, special_move == "big_castle")
            return

        new_row, new_col = new_position[1], new_position[0]
        old_row, old_col = piece.position.x, piece.position.y

        print(f"Moving piece {piece.pieceType} from ({old_row}, {old_col}) to ({new_row}, {new_col})")

        piece.position.x, piece.position.y = new_row, new_col

        self.board[new_row][new_col].piece = piece
        self.board[new_row][new_col].has_value = True
        self.board[old_row][old_col].piece = None
        self.board[old_row][old_col].has_value = False

        self.last_selected_piece = None
        self.possible_moves_list = None

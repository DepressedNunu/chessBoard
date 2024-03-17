import numpy as np

from src.Models.chess_square import ChessSquare
from src.Models.piece import Piece, PieceType, Position

starting_pieces_list = [
    Piece(PieceType.rookBlack, Position(0, 0)),
    Piece(PieceType.knightBlack, Position(0, 1)),
    Piece(PieceType.bishopBlack, Position(0, 2)),
    Piece(PieceType.queenBlack, Position(0, 3)),
    Piece(PieceType.kingBlack, Position(0, 4)),
    Piece(PieceType.bishopBlack, Position(0, 5)),
    Piece(PieceType.knightBlack, Position(0, 6)),
    Piece(PieceType.rookBlack, Position(0, 7)),
    Piece(PieceType.pawnBlack, Position(1, 0)),
    Piece(PieceType.pawnBlack, Position(1, 1)),
    Piece(PieceType.pawnBlack, Position(1, 2)),
    Piece(PieceType.pawnBlack, Position(1, 3)),
    Piece(PieceType.pawnBlack, Position(1, 4)),
    Piece(PieceType.pawnBlack, Position(1, 5)),
    Piece(PieceType.pawnBlack, Position(1, 6)),
    Piece(PieceType.pawnBlack, Position(1, 7)),
    Piece(PieceType.pawnWhite, Position(6, 0)),
    Piece(PieceType.pawnWhite, Position(6, 1)),
    Piece(PieceType.pawnWhite, Position(6, 2)),
    Piece(PieceType.pawnWhite, Position(6, 3)),
    Piece(PieceType.pawnWhite, Position(6, 4)),
    Piece(PieceType.pawnWhite, Position(6, 5)),
    Piece(PieceType.pawnWhite, Position(6, 6)),
    Piece(PieceType.pawnWhite, Position(6, 7)),
    Piece(PieceType.rookWhite, Position(7, 0)),
    Piece(PieceType.knightWhite, Position(7, 1)),
    Piece(PieceType.bishopWhite, Position(7, 2)),
    Piece(PieceType.queenWhite, Position(7, 3)),
    Piece(PieceType.kingWhite, Position(7, 4)),
    Piece(PieceType.bishopWhite, Position(7, 5)),
    Piece(PieceType.knightWhite, Position(7, 6)),
    Piece(PieceType.rookWhite, Position(7, 7)),

    # test purposes
    Piece(PieceType.pawnBlack, Position(5, 3))
]


class ChessBoard:
    def __init__(self):
        self.board = np.array([[ChessSquare(i, j) for j in range(8)] for i in range(8)], dtype=object)
        self.setup_pieces()

    def setup_pieces(self):
        for piece in starting_pieces_list:
            x, y = piece.position.x, piece.position.y
            square = self.board[x][y]
            square.piece = piece
            square.has_value = True

from enum import Enum

from src.Models.piece import Position, Piece


class Algebraic_piece_name(Enum):
    PAWN = ""
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"


class Move:
    # props
    initial_position: Position
    move_position: Position
    algebraic_notation: str
    color: bool
    score: int
    piece: Piece
    captured_piece: Piece

    def __init__(self, initial_position: Position, move_position: Position, piece: Piece,
                 captured_piece: Piece | None, score: int = 0) -> None:
        self.initial_position = initial_position
        self.move_position = move_position
        self.color = piece.color
        self.piece = piece
        self.score = score
        self.captured_piece = captured_piece

    def to_algebraic_notation(self):
        piece_letter = Algebraic_piece_name[self.piece.pieceType.name].value
        capture = ""
        if self.captured_piece is not None:
            if piece_letter == "":
                capture = chr(ord('a') + self.initial_position.y) + "x"
            else:
                capture = "x"

        self.algebraic_notation = piece_letter + capture + chr(ord('a') + self.move_position.y) + str(
            8 - self.move_position.x)
        return self.algebraic_notation

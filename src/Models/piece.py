from enum import Enum


class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Piece:
    def __getitem__(self, item):
        return self

    def __init__(self, piece_type: PieceType, position: Position, color: bool):
        self.color = color
        self.pieceType = piece_type
        self.position = position

        path_list = [
            "images/WHITE/white_pawn.png",
            "images/WHITE/white_tower.png",
            "images/WHITE/white_horse.png",
            "images/WHITE/white_bishop.png",
            "images/WHITE/white_queen.png",
            "images/WHITE/white_king.png",
            "images/BLACK/black_pawn.png",
            "images/BLACK/black_tower.png",
            "images/BLACK/black_horse.png",
            "images/BLACK/black_bishop.png",
            "images/BLACK/black_queen.png",
            "images/BLACK/black_king.png"
        ]
        if self.color:
            self.path = path_list[abs(piece_type.value) - 1]  # only the white pieces are negative
        else:
            self.path = path_list[abs(piece_type.value) - 1 + 6]

    def get_position(self):
        return self.position

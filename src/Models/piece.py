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
    pieceType = PieceType
    path = str()
    color = bool  # true = White

    def __getitem__(self, item):
        return self

    def __init__(self, piece_type: PieceType, color: bool, position: Position):
        self.color = color
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
        color_path = 0
        if not color:
            color_path = 6

        self.path = path_list[abs(piece_type.value) - 1 + color_path]
        self.pieceType = piece_type
        self.position = position

    def get_position(self):
        return self.position

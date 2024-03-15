from enum import Enum


class PieceType(Enum):
    PAWN_WHITE = -1
    ROOK_WHITE = -2
    KNIGHT_WHITE = -3
    BISHOP_WHITE = -4
    QUEEN_WHITE = -5
    KING_WHITE = -6
    PAWN_BLACK = 1
    ROOK_BLACK = 2
    KNIGHT_BLACK = 3
    BISHOP_BLACK = 4
    QUEEN_BLACK = 5
    KING_BLACK = 6



class Piece:
    pieceType = PieceType
    position = tuple()
    path = str()
    color = str()

    def __getitem__(self, item):
        return self

    def __init__(self, pieceType: PieceType, position: tuple):
        pathList = [
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
        if pieceType.value < 0:
            self.path = pathList[abs(pieceType.value) - 1]  # only the white pieces are negative
            self.color = "black"
        else:
            self.path = pathList[abs(pieceType.value) - 1 + 6]
            self.color = "white"
        self.pieceType = pieceType
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def get_position(self):
        return self.position
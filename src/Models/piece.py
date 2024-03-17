from enum import Enum


class PieceType(Enum):
    pawnWhite = -1
    rookWhite = -2
    knightWhite = -3
    bishopWhite = -4
    queenWhite = -5
    kingWhite = -6
    pawnBlack = 1
    rookBlack = 2
    knightBlack = 3
    bishopBlack = 4
    queenBlack = 5
    kingBlack = 6


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Piece:
    pieceType = PieceType
    path = str()
    color = str()

    def __getitem__(self, item):
        return self

    def __init__(self, piece_type: PieceType, position: Position):
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
        if piece_type.value < 0:
            self.path = path_list[abs(piece_type.value) - 1]  # only the white pieces are negative
            self.color = "black"
        else:
            self.path = path_list[abs(piece_type.value) - 1 + 6]
            self.color = "white"
        self.pieceType = piece_type
        self.position = position

    def get_position(self):
        return self.position

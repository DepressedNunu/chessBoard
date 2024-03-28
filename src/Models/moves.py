from enum import Enum

import pandas as pd

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

    def to_algebraic_notation(self) -> str:
        print(self.color)
        print(f"Position de mongoloer {self.initial_position.x}, {self.initial_position.y}")


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


class GameMoves:
    def __init__(self):
        self.move_list = pd.DataFrame({
            'Black': [],
            'White': [],
            'White_move_score': [],
            'Black_move_score': []
        }, columns=['White', 'Black', 'White_move_score', 'Black_move_score'])

    def add_move(self, move: Move):
        if move.color:  # if White
            new_row = [move.to_algebraic_notation(), None, move.score, None]
            self.move_list.loc[len(self.move_list)] = new_row
        else:
            self.move_list.at[self.move_list.index[-1], 'Black'] = move.to_algebraic_notation()
            self.move_list.at[self.move_list.index[-1], 'Black_move_score'] = move.score
        return self.move_list

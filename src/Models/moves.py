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

    def to_algebraic_notation(self, is_check: bool, is_checkmate: bool) -> str:
        piece_letter = Algebraic_piece_name[self.piece.pieceType.name].value
        capture = ""
        if self.captured_piece is not None:
            capture = "x"

        check_mate = ""
        check = ""
        if is_checkmate:
            check_mate = "#"
            check = ""

        self.algebraic_notation = piece_letter + capture + chr(ord('a') + self.move_position.y) + str(
            8 - self.move_position.x) + check_mate + check
        return self.algebraic_notation


class GameMoves:
    def __init__(self):
        self.move_df = pd.DataFrame(columns=['White', 'Black', 'White_move_score', 'Black_move_score'], index=['Turns'])
        self.df_import = pd.read_csv('saves/games_saves.csv', sep=';', index_col=0)

    def get_df_with_winner(self, move: Move):
        index = pd.MultiIndex.from_product([[1], ['Turns']], names=['Game', 'Info'])

        winner_df = pd.DataFrame({
            'White': ["winner" if move.color else "loser"],
            'Black': ["winner" if not move.color else "loser"]
        })

        self.move_df = pd.concat([self.move_df, winner_df])

        self.move_df.index = pd.MultiIndex.from_product([[1], self.move_df.index], names=['Game', 'Moves'])

        return self.move_df

    def insert_to_scv(self, move: Move):
        self.df_import = pd.concat([self.df_import, self.get_df_with_winner(move)])
        self.df_import.to_csv('saves/games_saves.csv', index=True, header=True, sep=';')

    def add_move(self, move: Move, is_check: bool, is_checkmate: bool):
        print(self.df_import)
        if is_checkmate:
            is_check = False
        if is_check:
            color = 'Black' if move.color else 'White'
            last_opponent_move = self.move_df.at[self.move_df.index[-1], color]
            self.move_df.at[self.move_df.index[-1], color] = last_opponent_move + "+"

        if move.color:
            # if White
            new_row = [move.to_algebraic_notation(is_check, is_checkmate), "None", move.score, None]
            if is_checkmate:
                self.move_df.loc[len(self.move_df) - 1] = new_row
            else:
                self.move_df.loc[len(self.move_df)] = new_row

        else:
            self.move_df.at[self.move_df.index[-1], 'Black'] = move.to_algebraic_notation(is_check, is_checkmate)
            self.move_df.at[self.move_df.index[-1], 'Black_move_score'] = move.score
        return self.move_df

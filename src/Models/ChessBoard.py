import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from src.Models.piece import Piece, PieceType


class ChessSquare(tk.Canvas):
    def __init__(self, master, color, piece=None, **kwargs):
        super().__init__(master, width=100, height=93, bg=color, **kwargs)
        self.piece = piece


class ChessBoard(tk.Frame):

    def __init__(self):
        super().__init__()

        # Variables
        self.is_highlighted = False
        self.possible_moves_list = None

        # Move variables
        self.new_position = None
        self.last_selected_piece = None

        # Get movement Functions
        self.movement_functions = {
            PieceType.PAWN_WHITE: self.pawn_possible_moves,
            PieceType.PAWN_BLACK: self.pawn_possible_moves,
            PieceType.ROOK_WHITE: self.rook_possible_moves,
            PieceType.ROOK_BLACK: self.rook_possible_moves,
            PieceType.KNIGHT_WHITE: self.knight_possible_moves,
            PieceType.KNIGHT_BLACK: self.knight_possible_moves,
            PieceType.BISHOP_WHITE: self.bishop_possible_moves,
            PieceType.BISHOP_BLACK: self.bishop_possible_moves,
            PieceType.QUEEN_WHITE: self.queen_possible_moves,
            PieceType.QUEEN_BLACK: self.queen_possible_moves,
            PieceType.KING_WHITE: self.king_possible_moves,
            PieceType.KING_BLACK: self.king_possible_moves
        }

        # Default Placement of the pieces
        self.pieces_list = [
            Piece(PieceType.ROOK_BLACK, (0, 0)),
            Piece(PieceType.KNIGHT_BLACK, (0, 1)),
            Piece(PieceType.BISHOP_BLACK, (0, 2)),
            Piece(PieceType.QUEEN_BLACK, (0, 3)),
            Piece(PieceType.KING_BLACK, (0, 4)),
            Piece(PieceType.BISHOP_BLACK, (0, 5)),
            Piece(PieceType.KNIGHT_BLACK, (0, 6)),
            Piece(PieceType.ROOK_BLACK, (0, 7)),
            Piece(PieceType.PAWN_BLACK, (1, 0)),
            Piece(PieceType.PAWN_BLACK, (1, 1)),
            Piece(PieceType.PAWN_BLACK, (1, 2)),
            Piece(PieceType.PAWN_BLACK, (1, 3)),
            Piece(PieceType.PAWN_BLACK, (1, 4)),
            Piece(PieceType.PAWN_BLACK, (1, 5)),
            Piece(PieceType.PAWN_BLACK, (1, 6)),
            Piece(PieceType.PAWN_BLACK, (1, 7)),
            Piece(PieceType.PAWN_WHITE, (6, 0)),
            Piece(PieceType.PAWN_WHITE, (6, 1)),
            Piece(PieceType.PAWN_WHITE, (6, 2)),
            Piece(PieceType.PAWN_WHITE, (6, 3)),
            Piece(PieceType.PAWN_WHITE, (6, 4)),
            Piece(PieceType.PAWN_WHITE, (6, 5)),
            Piece(PieceType.PAWN_WHITE, (6, 6)),
            Piece(PieceType.PAWN_WHITE, (6, 7)),
            Piece(PieceType.ROOK_WHITE, (7, 0)),
            Piece(PieceType.KNIGHT_WHITE, (7, 1)),
            Piece(PieceType.BISHOP_WHITE, (7, 2)),
            Piece(PieceType.QUEEN_WHITE, (7, 3)),
            Piece(PieceType.KING_WHITE, (7, 4)),
            Piece(PieceType.BISHOP_WHITE, (7, 5)),
            Piece(PieceType.KNIGHT_WHITE, (7, 6)),
            Piece(PieceType.ROOK_WHITE, (7, 7)),

            # test purposes
            Piece(PieceType.PAWN_BLACK, (5, 3))
        ]

        # colors
        self.white_square = "#18D9AC"
        self.black_square = "#BED8D2"
        self.highlight_square = "#91C73B"

        # create the chess board Data
        self.chessData = np.array([[None for i in range(8)] for j in range(8)])  # Keep track of the pieces class
        for piece in self.pieces_list:
            self.place_piece(piece)
        self.chessSquares = [[None] * 8 for _ in range(8)]  # Keep track of ChessSquare instances

    def place_piece(self, piece: Piece):
        self.chessData[piece.position[0]][piece.position[1]] = piece

    def is_empty_square(self, row, col):
        return self.is_valid_position(row, col) and self.chessData[row][col] is None

    def is_enemy_piece(self, row, col, color):
        return self.is_valid_position(row, col) and self.chessData[row][col] is not None and self.chessData[row][
            col].color != color

    @staticmethod
    def is_valid_position(row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def pawn_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        pawn_direction = 1 if piece.color == 'white' else -1
        if self.is_empty_square(row + pawn_direction, col):
            self.possible_moves_list.append((row + pawn_direction, col))
            if (row == 1 and piece.color == 'white') or (row == 6 and piece.color == 'black'):
                if self.is_empty_square(row + 2 * pawn_direction, col):
                    self.possible_moves_list.append((row + 2 * pawn_direction, col))

        for dcol in [-1, 1]:
            new_row, new_col = row + pawn_direction, col + dcol
            if self.is_valid_position(new_row, new_col) and self.is_enemy_piece(new_row, new_col, piece.color):
                self.possible_moves_list.append((new_row, new_col))
        return self.possible_moves_list

    def rook_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col):
                        self.possible_moves_list.append((new_row, new_col))
                    elif self.is_enemy_piece(new_row, new_col, piece.color):
                        self.possible_moves_list.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return self.possible_moves_list

    def knight_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
        for drow, dcol in moves:
            new_row, new_col = row + drow, col + dcol
            if self.is_valid_position(new_row, new_col) and (
                    self.is_empty_square(new_row, new_col) or self.is_enemy_piece(new_row, new_col, piece.color)):
                self.possible_moves_list.append((new_row, new_col))
        return self.possible_moves_list

    def bishop_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col):
                        self.possible_moves_list.append((new_row, new_col))
                    elif self.is_enemy_piece(new_row, new_col, piece.color):
                        self.possible_moves_list.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return self.possible_moves_list

    def queen_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if self.is_valid_position(new_row, new_col):
                    if self.is_empty_square(new_row, new_col):
                        self.possible_moves_list.append((new_row, new_col))
                    elif self.is_enemy_piece(new_row, new_col, piece.color):
                        self.possible_moves_list.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return self.possible_moves_list

    def king_possible_moves(self, piece: Piece):
        row, col = piece.position
        self.possible_moves_list = []
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for drow, dcol in moves:
            new_row, new_col = row + drow, col + dcol
            if self.is_valid_position(new_row, new_col) and (
                    self.is_empty_square(new_row, new_col) or self.is_enemy_piece(new_row, new_col, piece.color)):
                self.possible_moves_list.append((new_row, new_col))
        return self.possible_moves_list

    def highlight_moves(self, moves):
        if self.is_highlighted:
            self.unhighlight_moves()
        for move in moves:
            row, col = move
            self.chessSquares[row][col].config(bg=self.highlight_square)
            self.is_highlighted = True

    def unhighlight_moves(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.white_square
                else:
                    color = self.black_square
                self.chessSquares[i][j].config(bg=color)

    def draw_board(self, root):
        for i in range(8):
            for j in range(8):
                color = self.white_square if (i + j) % 2 == 0 else self.black_square
                square = ChessSquare(root, color)
                square.grid(row=i, column=j)
                self.chessSquares[i][j] = square

                # Add coordinate text on the square
                coordinate_label = tk.Label(square, text=f"{i},{j}", font=("Arial", 8))
                coordinate_label.place(relx=0.5, rely=0.1, anchor="center")

                if self.chessData[i][j] is not None:  # if there is a piece in the position
                    piece = self.chessData[i][j]
                    img = Image.open(piece.path)
                    photo = ImageTk.PhotoImage(img)
                    # put the picture in the center of the square
                    square.create_image(50, 46, image=photo)
                    square.photo = photo
                    square.piece = piece
                    if self.last_selected_piece is not None and self.last_selected_piece == piece:
                        square.config(bg="blue")
                    if self.possible_moves_list is None and square.cget("bg") != "green":
                        square.bind("<Button-1>", self.detect_piece_position)
                else:
                    square.bind("<Button-1>", self.move_piece)

        root.mainloop()

    def detect_piece_position(self, event):
        square = event.widget
        piece = square.piece

        if self.last_selected_piece is not None:
            if piece.color != self.last_selected_piece.color:
                self.move_piece(event)
        piece.position = event.widget.grid_info()["row"], event.widget.grid_info()[
            "column"]  # update the piece position
        self.last_selected_piece = piece
        self.possible_moves_list = self.movement_functions[piece.pieceType](piece)
        self.highlight_moves(self.possible_moves_list)

    def move_piece(self, event):
        square = event.widget
        if self.possible_moves_list is not None:
            self.new_position = (square.grid_info()["row"], square.grid_info()["column"])
            # detect if the square clicked is in the possible moves list
            if self.new_position in self.possible_moves_list:
                self.chessData[self.new_position[0]][self.new_position[1]] = self.last_selected_piece
                self.chessData[self.last_selected_piece.position[0]][self.last_selected_piece.position[1]] = None

                # reset the variables
                self.possible_moves_list = None
                self.last_selected_piece = None
                self.new_position = None
                self.draw_board(self.master)

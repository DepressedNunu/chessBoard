import numpy
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from Models.piece import *


class ChessSquare(tk.Canvas):
    def __init__(self, master, color, piece=None, **kwargs):
        super().__init__(master, width=100, height=93, bg=color, **kwargs)
        self.piece = piece


class ChessBoard(tk.Frame):
    is_highlighted = False
    pieceClicked = False

    def __init__(self):
        super().__init__()
        self.image = None
        self.pieces_list = [
            Piece(PieceType.rookBlack, (0, 0)),
            Piece(PieceType.knightBlack, (0, 1)),
            Piece(PieceType.bishopBlack, (0, 2)),
            Piece(PieceType.queenBlack, (0, 3)),
            Piece(PieceType.kingBlack, (0, 4)),
            Piece(PieceType.bishopBlack, (0, 5)),
            Piece(PieceType.knightBlack, (0, 6)),
            Piece(PieceType.rookBlack, (0, 7)),
            Piece(PieceType.pawnBlack, (1, 0)),
            Piece(PieceType.pawnBlack, (1, 1)),
            Piece(PieceType.pawnBlack, (1, 2)),
            Piece(PieceType.pawnBlack, (1, 3)),
            Piece(PieceType.pawnBlack, (1, 4)),
            Piece(PieceType.pawnBlack, (1, 5)),
            Piece(PieceType.pawnBlack, (1, 6)),
            Piece(PieceType.pawnBlack, (1, 7)),
            Piece(PieceType.pawnWhite, (6, 0)),
            Piece(PieceType.pawnWhite, (6, 1)),
            Piece(PieceType.pawnWhite, (6, 2)),
            Piece(PieceType.pawnWhite, (6, 3)),
            Piece(PieceType.pawnWhite, (6, 4)),
            Piece(PieceType.pawnWhite, (6, 5)),
            Piece(PieceType.pawnWhite, (6, 6)),
            Piece(PieceType.pawnWhite, (6, 7)),
            Piece(PieceType.rookWhite, (7, 0)),
            Piece(PieceType.knightWhite, (7, 1)),
            Piece(PieceType.bishopWhite, (7, 2)),
            Piece(PieceType.queenWhite, (7, 3)),
            Piece(PieceType.kingWhite, (7, 4)),
            Piece(PieceType.bishopWhite, (7, 5)),
            Piece(PieceType.knightWhite, (7, 6)),
            Piece(PieceType.rookWhite, (7, 7)),

            #test purposes
            Piece(PieceType.pawnBlack, (5, 3))
        ]
        self.chessData = np.array([[None for i in range(8)] for j in range(8)])  # Keep track of the pieces class
        for piece in self.pieces_list:
            self.place_piece(piece)
        self.chessSquares = [[None] * 8 for _ in range(8)]  # Keep track of ChessSquare instances

    def place_piece(self, piece: Piece):
        self.chessData[piece.position[0]][piece.position[1]] = piece

    def move_piece(self, piece: Piece, new_position: tuple):
        self.chessData[piece.position[0]][piece.position[1]] = None
        piece.move(new_position)
        self.chessData[new_position[0]][new_position[1]] = piece

    def possible_moves(self, piece: Piece, chess_data):
        possible_moves = []

        def is_valid_position(row, col):
            return 0 <= row < 8 and 0 <= col < 8

        def is_empty_square(row, col):
            return is_valid_position(row, col) and chess_data[row][col] is None

        def is_enemy_piece(row, col, color):
            return is_valid_position(row, col) and chess_data[row][col] is not None and chess_data[row][col].color != color

        row, col = piece.position

        if piece.pieceType == PieceType.pawnWhite:
            # Check forward moves
            if is_empty_square(row - 1, col):
                possible_moves.append((row - 1, col))
                if row == 6 and is_empty_square(row - 2, col):
                    possible_moves.append((row - 2, col))

            # Check diagonal captures
            if is_enemy_piece(row - 1, col - 1, "red"):
                possible_moves.append((row - 1, col - 1))
            if is_enemy_piece(row - 1, col + 1, "red"):
                possible_moves.append((row - 1, col + 1))

        self.highlight_moves(possible_moves)
        return possible_moves

    def highlight_moves(self, moves):
        if self.is_highlighted:
            self.unhighlight_moves()
        for move in moves:
            row, col = move
            self.chessSquares[row][col].config(bg="green")
            self.is_highlighted = True

    def unhighlight_moves(self):
        print("unhighlighting")
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = "white"
                else:
                    color = "black"
                self.chessSquares[i][j].config(bg=color)

    def draw_board(self, root, pieceClicked=False):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = "white"
                else:
                    color = "black"
                if self.chessData[i][j] is not None:
                    piece = self.chessData[i][j]
                    img = ImageTk.PhotoImage(Image.open(piece.path))
                    square = ChessSquare(root, color, piece=piece)
                    square.create_image(50, 50, anchor=tk.CENTER, image=img)
                    square.image = img  # Keep a reference to the image to prevent garbage collection
                    square.bind("<Button-1>", lambda event, p=piece: self.possible_moves(p, self.chessData)) # Detect clicks
                    square.grid(row=i, column=j)
                    self.chessSquares[i][j] = square
                else:
                    square = ChessSquare(root, color)
                    square.grid(row=i, column=j)
                    self.chessSquares[i][j] = square
                    square.bind("<Button-1>", lambda event, p=piece: self.possible_moves(p, self.chessData)) # Detect clicks
        root.mainloop()

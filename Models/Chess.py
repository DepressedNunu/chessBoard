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

    def __init__(self):
        super().__init__()

        # Variables
        self.is_highlighted = False
        self.possible_moves_list = None

        # Move variables
        self.new_position = None
        self.last_selected_piece = None
        self.image = None

        # Default Placement of the pieces
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

            # test purposes
            Piece(PieceType.pawnBlack, (5, 3))
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

    def possible_moves(self, piece: Piece):
        possible_moves = []

        def is_valid_position(row, col):
            return 0 <= row < 8 and 0 <= col < 8

        def is_empty_square(row, col):
            return is_valid_position(row, col) and self.chessData[row][col] is None

        def is_enemy_piece(row, col):
            return is_valid_position(row, col) and self.chessData[row][col] is not None and self.chessData[row][
                col].color != self.last_selected_piece.color

        def is_ally_piece(row, col):
            return is_valid_position(row, col) and self.chessData[row][col] is not None and self.chessData[row][
                col].color == self.last_selected_piece.color

        row, col = piece.position

        if piece.pieceType == PieceType.pawnWhite:
            if is_empty_square(row - 1, col):
                possible_moves.append((row - 1, col))
                if row == 6 and is_empty_square(row - 2, col):
                    possible_moves.append((row - 2, col))

            if is_enemy_piece(row - 1, col - 1):
                possible_moves.append((row - 1, col - 1))
            if is_enemy_piece(row - 1, col + 1):
                possible_moves.append((row - 1, col + 1))

        if piece.pieceType == PieceType.pawnBlack:
            if is_empty_square(row + 1, col):
                possible_moves.append((row + 1, col))
                if row == 1 and is_empty_square(row + 2, col):
                    possible_moves.append((row + 2, col))

            if is_enemy_piece(row + 1, col - 1):
                possible_moves.append((row + 1, col - 1))
            if is_enemy_piece(row + 1, col + 1):
                possible_moves.append((row + 1, col + 1))

        if piece.pieceType == PieceType.rookBlack or piece.pieceType == PieceType.rookWhite:
            for coef1, coef2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for x in range(1, 8):
                    for y in range(1, 8):
                        if is_empty_square(row + x * coef1, col + y * coef2):
                            possible_moves.append((row + x * coef1, col + y * coef2))
                        elif is_ally_piece(row + x * coef1, col + y * coef2, piece.color):
                            break
                        else:
                            if is_enemy_piece(row + x * coef1, col + y * coef2):
                                possible_moves.append((row + x * coef1, col + y * coef2))
                            break
                        break
                    break
        if piece.pieceType == PieceType.knightBlack or piece.pieceType == PieceType.knightWhite:
            for coef1, coef2 in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]:
                if is_empty_square(row + coef1, col + coef2):
                    possible_moves.append((row + coef1, col + coef2))
                elif is_ally_piece(row + coef1, col + coef2, piece.color):
                    break
                else:
                    if is_enemy_piece(row + coef1, col + coef2, piece.color):
                        possible_moves.append((row + coef1, col + coef2))
                    break
                break

        if piece.pieceType == PieceType.bishopBlack or piece.pieceType == PieceType.bishopWhite:
            for coef1, coef2 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                for i in range(1, 8):
                    for j in range(1, 8):
                        if is_empty_square(row + i * coef1, col + j * coef2):
                            possible_moves.append((row + i * coef1, col + j * coef2))
                        elif is_ally_piece(row + i * coef1, col + j * coef2):
                            break
                        else:
                            if is_enemy_piece(row + i * coef1, col + j * coef2):
                                possible_moves.append((row + i * coef1, col + j * coef2))
                            break
                        break
                    break

        if piece.pieceType == PieceType.queenBlack or piece.pieceType == PieceType.queenWhite:
            for coef1, coef2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for x in range(1, 8):
                    for y in range(1, 8):
                        if is_empty_square(row + x * coef1, col + y * coef2):
                            possible_moves.append((row + x * coef1, col + y * coef2))
                        elif is_ally_piece(row + x * coef1, col + y * coef2):
                            break
                        else:
                            if is_enemy_piece(row + x * coef1, col + y * coef2):
                                possible_moves.append((row + x * coef1, col + y * coef2))
                            break
                        break
                    break
            for coef1, coef2 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                for i in range(1, 8):
                    for j in range(1, 8):
                        if is_empty_square(row + i * coef1, col + j * coef2):
                            possible_moves.append((row + i * coef1, col + j * coef2))
                        elif is_ally_piece(row + i * coef1, col + j * coef2, piece.color):
                            break
                        else:
                            if is_enemy_piece(row + i * coef1, col + j * coef2, piece.not_color):
                                possible_moves.append((row + i * coef1, col + j * coef2))
                            break
                        break
                    break

        if piece.pieceType == PieceType.kingBlack or piece.pieceType == PieceType.kingWhite:
            for coef1, coef2 in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                if is_empty_square(row + coef1, col + coef2):
                    possible_moves.append((row + coef1, col + coef2))
                elif is_ally_piece(row + coef1, col + coef2, piece.color):
                    break
                else:
                    if is_enemy_piece(row + coef1, col + coef2, piece.not_color):
                        possible_moves.append((row + coef1, col + coef2))
                    break
                break

        return possible_moves

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
        piece.position = event.widget.grid_info()["row"], event.widget.grid_info()["column"] # update the piece position
        self.last_selected_piece = piece
        self.possible_moves_list = self.possible_moves(piece)
        self.highlight_moves(self.possible_moves_list)

    def move_piece(self, event):
        if self.is_highlighted:
            self.unhighlight_moves()
        square = event.widget
        if self.possible_moves_list is not None:
            # detect if the square clicked is in the possible moves list
            self.new_position = (square.grid_info()["row"], square.grid_info()["column"])
            if self.new_position in self.possible_moves_list:
                self.chessData[self.new_position[0]][self.new_position[1]] = self.last_selected_piece
                self.chessData[self.last_selected_piece.position[0]][self.last_selected_piece.position[1]] = None

                # reset the variables
                self.possible_moves_list = None
                self.last_selected_piece = None
                self.new_position = None

                self.draw_board(self.master)

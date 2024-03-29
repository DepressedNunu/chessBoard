import time
import tkinter as tk

import pandas as pd
from PIL import Image, ImageTk

from src.Models import chess_board
from src.Models.chess_square import ChessSquare
from src.Models.ia import ia
from src.Models.piece import Piece, PieceType

white_square = "#BED8D2"
black_square = "#18D9AC"
highlight_square = "#91C73B"


def set_color(position_x: int, position_y: int) -> str:
    return white_square if (position_x + position_y) % 2 == 0 else black_square


class SquareCanvas(tk.Canvas):
    def __init__(self, master, chess_square: ChessSquare, click_callback):
        super().__init__(master, width=100, height=100, background=set_color(chess_square.x, chess_square.y))
        # Variables
        self.piece_image = None
        self.is_highlighted = False

        self.chess_square = chess_square
        self.position_x = chess_square.x
        self.position_y = chess_square.y
        self.click_callback = click_callback
        if chess_square.has_value:
            self.display_piece(chess_square.piece)
        # Add coordinates text
        self.create_text(50, 10, text=f"x:{self.position_x},y:{self.position_y}",
                         font=("Arial", 12), fill="black")

        # Listen click
        self.bind("<Button-1>", self.on_square_clicked)

    def display_piece(self, piece: Piece):
        image = Image.open(piece.path)
        image = image.resize((70, 70), Image.Resampling.LANCZOS)
        self.piece_image = ImageTk.PhotoImage(image)
        self.create_image(50, 50, image=self.piece_image)

    def on_square_clicked(self, event):
        self.click_callback(self)


class BoardCanvas(tk.Canvas):
    def __init__(self, master, h, w, click_callback):
        super().__init__(master)
        self.configure(width=w, height=h)
        self.grid(row=1, column=1)
        self.click_callback = click_callback

    def add_square(self, chess_square: ChessSquare, click_callback):
        square = SquareCanvas(self, chess_square, click_callback)
        square.grid(row=chess_square.y, column=chess_square.x)


class BoardWindow(tk.Tk):
    def __init__(self, chess_board: chess_board):
        super().__init__()
        self.df_text = None
        self.chess_board = chess_board
        self.possible_moves_list = []
        self.state("zoomed")

        # test IA
        self.ia = ia(chess_board)

        self.movement_functions = {
            PieceType.PAWN_WHITE: self.chess_board.pawn_possible_moves,
            PieceType.PAWN_BLACK: self.chess_board.pawn_possible_moves,
            PieceType.ROOK_WHITE: self.chess_board.rook_possible_moves,
            PieceType.ROOK_BLACK: self.chess_board.rook_possible_moves,
            PieceType.KNIGHT_WHITE: self.chess_board.knight_possible_moves,
            PieceType.KNIGHT_BLACK: self.chess_board.knight_possible_moves,
            PieceType.BISHOP_WHITE: self.chess_board.bishop_possible_moves,
            PieceType.BISHOP_BLACK: self.chess_board.bishop_possible_moves,
            PieceType.QUEEN_WHITE: self.chess_board.queen_possible_moves,
            PieceType.QUEEN_BLACK: self.chess_board.queen_possible_moves,
            PieceType.KING_WHITE: self.chess_board.king_possible_moves,
            PieceType.KING_BLACK: self.chess_board.king_possible_moves
        }

        self.new_position = None
        self.last_selected_piece = None

        self.title("Chess Board")
        self.board = BoardCanvas(self, 800, 800, self.handle_square_click)
        self.create_board(chess_board)

        self.create_menu()
        df = pd.DataFrame({'A': [9, 50], 'B': [51, 92]}, index=[1, 2])
        self.create_df_affichage(df)

        self.turn_label = tk.Label(self, text=f"Turn: {'White' if self.chess_board.turn else 'Black'}",
                                   font=("Arial", 16))
        self.turn_label.grid(row=0, column=1)

    def create_menu(self):
        menu_frame = tk.Frame(self)
        menu_frame.grid(row=0, column=0, rowspan=2, padx=20)

        jvj_button = tk.Button(menu_frame, text="Player vs Player")
        jvj_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        jvia_button = tk.Button(menu_frame, text="Player vs AI")
        jvia_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        iavia_button = tk.Button(menu_frame, text="AI vs AI")
        iavia_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    def create_df_affichage(self, df):
        self.df_frame = tk.Frame(self)
        self.df_frame.grid(row=0, column=2, rowspan= 2, ipadx= 10)

        df_label = tk.Label(self.df_frame, text="Dataframe")
        df_label.grid(row=0, column=0)

        self.df_text = tk.Text(self.df_frame, height=50, width=30)
        self.df_text.grid(row=1, column=0)
        self.df_text.insert(tk.END, df.to_string())
        self.df_text.config(state=tk.DISABLED)

    def create_board(self, board: chess_board):
        for i in range(8):
            for j in range(8):
                self.board.add_square(board.board[i][j], self.handle_square_click)

    def highlight_squares(self):
        self.unhighlight_squares()
        for row in range(8):
            for col in range(8):
                square_canvas = self.board.grid_slaves(row, col)[0]
                if (square_canvas.position_y, square_canvas.position_x) in self.possible_moves_list:
                    square_canvas.config(background=highlight_square)

    def unhighlight_squares(self):
        for row in range(8):
            for col in range(8):
                square_canvas = self.board.grid_slaves(row, col)[0]
                square_canvas.config(background=set_color(square_canvas.position_x, square_canvas.position_y))

    def handle_square_click(self, square_canvas):
        self.display_possible_positions(square_canvas)

        if self.last_selected_piece and self.last_selected_piece is not square_canvas:  # If a piece is selected
            self.last_selected_piece.is_highlighted = False  # Unselect the last piece
            self.last_selected_piece.config(
                background=set_color(self.last_selected_piece.position_x, self.last_selected_piece.position_y))
            print(self.possible_moves_list)
            if self.possible_moves_list:
                if (square_canvas.position_y, square_canvas.position_x) in self.possible_moves_list:
                    self.chess_board.move(self.last_selected_piece.chess_square.piece,
                                          (square_canvas.position_y, square_canvas.position_x))
                    self.create_board(self.chess_board)
                    self.chess_board.turn = not self.chess_board.turn

                    # IA move
                    # self.ia.play(self.chess_board, self.chess_board.get_pieces(self.chess_board.turn))
                    # self.create_board(self.chess_board)
                    # self.chess_board.turn = not self.chess_board.turn

        if self.chess_board.is_checkmate(self.chess_board.turn):
            print("Checkmate!!!!!!!!!!!!!!!!!!!!!!!!")
            checkmate_window = tk.Tk()
            checkmate_window.title("Checkmate")
            checkmate_window.geometry("200x200")
            checkmate_label = tk.Label(checkmate_window, text="Checkmate!")
            checkmate_label.pack()
            checkmate_window.mainloop()

    def display_possible_positions(self, square_canvas):
        if square_canvas.chess_square.has_value and square_canvas.chess_square.piece.color == self.chess_board.turn:
            self.last_selected_piece = square_canvas
            self.last_selected_piece.is_highlighted = True

            # retrieve all the movements
            self.possible_moves_list = self.movement_functions[
                self.last_selected_piece.chess_square.piece.pieceType](
                self.last_selected_piece.chess_square.piece)
            self.possible_moves_list = self.chess_board.filter_possible_moves(
                self.last_selected_piece.chess_square.piece)
            self.highlight_squares()
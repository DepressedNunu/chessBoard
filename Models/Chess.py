import tkinter as tk


class ChessSquare(tk.Canvas):
    def __init__(self, master, color, piece=None, **kwargs):
        super().__init__(master, width=100, height=93, bg=color, **kwargs)
        self.piece = piece

        if self.piece:
            self.add_piece()

    def add_piece(self):
        color = "BLACK" if self.piece < 0 else "WHITE"
        piece_type = abs(self.piece)
        image_path = f"images/{color}/{color.lower()}_{'pawn' if piece_type == 1 else 'king' if piece_type == 6 else 'queen' if piece_type == 5 else 'bishop' if piece_type == 3 else 'horse' if piece_type == 4 else 'tower'}.png"
        self.image = tk.PhotoImage(file=image_path)
        self.create_image(50, 50, image=self.image)


class ChessBoard(tk.Frame):
    chessboard = [
        [-2, -3, -4, -5, -6, -4, -3, -2],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 3, 4, 5, 6, 4, 3, 2],
    ]

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.create_board()

    def create_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                piece = self.chessboard[j][i]
                square = ChessSquare(self.root, color, piece, highlightthickness=0)
                square.grid(row=j, column=i, padx=1, pady=1)

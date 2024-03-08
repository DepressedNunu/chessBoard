import tkinter as tk


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
        super().__init__()
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.draw_board_cases()

    def draw_board_cases(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill="white")
                else:
                    self.canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill="black")

    def link_pieces_to_board(self):
        for i in range(8):
            for j in range(8):
                if self.chessboard[i][j] == -2:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_tower)
                elif self.chessboard[i][j] == -3:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_bishop)
                elif self.chessboard[i][j] == -4:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_horse)
                elif self.chessboard[i][j] == -5:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_queen)
                elif self.chessboard[i][j] == -6:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_king)
                elif self.chessboard[i][j] == -1:
                    self.canvas.create_image(i * 50, j * 50, image=self.black_pawn)
                elif self.chessboard[i][j] == 1:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_pawn)
                elif self.chessboard[i][j] == 2:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_tower)
                elif self.chessboard[i][j] == 3:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_bishop)
                elif self.chessboard[i][j] == 4:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_horse)
                elif self.chessboard[i][j] == 5:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_queen)
                elif self.chessboard[i][j] == 6:
                    self.canvas.create_image(i * 50, j * 50, image=self.white_king)
                else:
                    pass

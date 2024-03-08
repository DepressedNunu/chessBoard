from Models import Chess
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = Chess.ChessBoard(root)
    app.mainloop()

from src.Models.chess_board import ChessBoard
from src.display.board import BoardWindow

if __name__ == "__main__":
    chess_board = ChessBoard()
    app = BoardWindow(chess_board)
    app.mainloop()

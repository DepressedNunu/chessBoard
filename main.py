from src.Models.chess_board import ChessBoard
from src_view.board import BoardWindow

if __name__ == "__main__":
    chess_board = ChessBoard()
    app = BoardWindow(chess_board)
    app.mainloop()
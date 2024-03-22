from src.Models.chess_board import ChessBoard
from src_view.board import BoardWindow
from src.Models.ia import ChessIa
if __name__ == "__main__":
    chess_board = ChessBoard()
    app = BoardWindow(chess_board)
    app.mainloop()
    ChessIa = ChessIa(chess_board)
    ChessIa.get_best_move()
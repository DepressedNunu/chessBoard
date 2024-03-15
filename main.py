from src.Models.ChessBoard import ChessBoard
from src.Models.piece import Piece
from src.Models.piece import PieceType

if __name__ == '__main__':
    board = ChessBoard()
    board.display_board()
    print("\n===========================================\n")
    pawn = Piece(PieceType.pawnBlack, (1, 1))
    print(pawn.pieceType.value)
    print(pawn.path)
class ChessSquare:
    def __init__(self, x: int, y: int, piece=None) -> None:
        self.x: int = x
        self.y: int = y
        self.has_value = False
        self.piece = piece

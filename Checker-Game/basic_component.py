from enums import PiecePlayer, PieceType, Color

class Place:
    def __init__(self, name, color: Color, occupant=None):
        self.name = name
        self.occupant = occupant
        self.color = color

    def is_available(self):
        return self.occupant is None

    def remove_occupant(self):
        occup = self.occupant
        self.occupant = None
        return occup

    def add_occupant(self, piece):
        if self.is_available():
            self.occupant = piece
            return True
        return False


class Piece:
    def __init__(self, player: PiecePlayer, type: PieceType):
        self.type = type
        self.player = player

    def make_king(self):
        self.type = PieceType.KING.value
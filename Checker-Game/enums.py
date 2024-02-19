from enum import Enum

class Color(Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'
class PieceType(Enum):
    KING = 'king  '
    NORMAL = 'normal'

class PiecePlayer(Enum):
    FIRST_PLAYER = 'P1'
    SECOND_PLAYER = 'P2'
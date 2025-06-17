from .frame import Frame
from .polygon_piece import PolygonPiece


class Placement:
    def __init__(
        self, piece: PolygonPiece, frame: Frame, position: tuple[float, float]
    ):
        self.piece = piece
        self.frame = frame
        self.position = position

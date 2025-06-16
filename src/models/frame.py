from shapely.geometry import Polygon

from .polygon_piece import PolygonPiece


class Frame:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.polygon = Polygon([(0, 0), (width, 0), (width, height), (0, height)])

    def contains(self, piece: PolygonPiece):
        return self.polygon.contains(piece.polygon)

    def copy(self):
        return Frame(self.width, self.height)

import copy
import os

from shapely import Polygon
from shapely.affinity import translate


EDGE_SEPARATOR = "::::"
EDGES_SEPARATOR = "::"


class PolygonPiece:
    def __init__(
        self,
        name: str,
        vertices: list[tuple[float, float]],
        width: float = 1.0,
        height: float = 1.0,
    ):
        self.name = name
        self.vertices = vertices
        self.width = width
        self.height = height
        self.polygon = Polygon(vertices)

    def scale_to_unit(self):
        xs, ys = zip(*self.vertices)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x
        height = max_y - min_y
        scale = 1.0 / max(width, height)
        self.vertices = [
            ((x - min_x) * scale, (y - min_y) * scale) for x, y in self.vertices
        ]
        self.polygon = Polygon(self.vertices)

    def create_instance(self, width: float, height: float):
        new_piece = PolygonPiece(
            name=self.name,
            vertices=copy.deepcopy(self.vertices),
            width=width,
            height=height,
        )
        new_piece.scale_to_size(width, height)
        return new_piece

    def move(self, dx, dy):
        moved_poly = translate(self.polygon, dx, dy)
        return PolygonPiece(self.name, list(moved_poly.exterior.coords)[:-1])

    def reflect(self):
        reflected = [(-x, -y) for (x, y) in self.vertices]
        return PolygonPiece(self.name, reflected)

    def save_to_txt(self, filepath: str):
        self.scale_to_unit()
        new_line = f"{self.name}{EDGE_SEPARATOR}{EDGES_SEPARATOR.join(f'({x},{y})' for x, y in self.vertices)}\n"
        lines: list[str] = []
        found = False
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                for line in f:
                    if line.startswith(f"{self.name}{EDGE_SEPARATOR}"):
                        lines.append(new_line)
                        found = True
                    else:
                        lines.append(line)

        if not found:
            lines.append(new_line)

        with open(filepath, "w") as f:
            f.writelines(lines)

    def scale_to_size(self, target_width: float, target_height: float):
        xs, ys = zip(*self.vertices)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x
        height = max_y - min_y
        scale = min(target_width / width, target_height / height)
        self.vertices = [
            ((x - min_x) * scale, (y - min_y) * scale) for x, y in self.vertices
        ]
        self.polygon = Polygon(self.vertices)

    @staticmethod
    def load_from_txt(filepath: str):
        pieces = []
        with open(filepath, "r") as f:
            for line in f:
                name, verts_str = line.strip().split(EDGE_SEPARATOR)
                verts = []
                for v in verts_str.split(EDGES_SEPARATOR):
                    if v.startswith("(") and v.endswith(")"):
                        x, y = v[1:-1].split(",")
                        verts.append((float(x), float(y)))

                pieces.append(PolygonPiece(name, verts))

        return pieces

from shapely.affinity import translate
from shapely import union_all

from src.models import PolygonPiece, Frame


class NFPComputer:
    """
    Clase utilitaria para el cálculo de No-Fit Polygon (NFP) y posiciones factibles de piezas poligonales.
    """

    @staticmethod
    def minkowski_sum(fixed: PolygonPiece, moving: PolygonPiece):
        """
        Calcula la suma de Minkowski entre dos polígonos.

        :param fixed: Pieza poligonal fija.
        :type fixed: PolygonPiece
        :param moving: Pieza poligonal móvil (ya reflejada si corresponde).
        :type moving: PolygonPiece
        :return: Polígono resultante de la suma de Minkowski.
        :rtype: shapely.geometry.Polygon o MultiPolygon
        """
        result = []
        for bx, by in moving.vertices:
            moved = translate(fixed.polygon, bx, by)
            result.append(moved)

        union = union_all(result)
        return union

    @staticmethod
    def compute_nfp(fixed: PolygonPiece, moving: PolygonPiece):
        """
        Calcula el No-Fit Polygon (NFP) entre dos piezas poligonales.

        :param fixed: Pieza poligonal fija.
        :type fixed: PolygonPiece
        :param moving: Pieza poligonal móvil.
        :type moving: PolygonPiece
        :return: Polígono NFP resultante.
        :rtype: shapely.geometry.Polygon o MultiPolygon
        """
        moving_reflected = moving.reflect()
        nfp = NFPComputer.minkowski_sum(fixed, moving_reflected)
        return nfp

    @staticmethod
    def feasible_positions(
        frame: Frame,
        placed_pieces: list[PolygonPiece],
        moving_piece: PolygonPiece,
    ):
        """
        Devuelve una lista de posiciones factibles (x, y) donde se puede colocar la pieza móvil
        dentro del marco sin solaparse con las piezas ya colocadas.

        :param frame: Marco rectangular donde se colocan las piezas.
        :type frame: Frame
        :param placed_pieces: Lista de piezas ya colocadas en el marco.
        :type placed_pieces: list[PolygonPiece]
        :param moving_piece: Pieza poligonal a colocar.
        :type moving_piece: PolygonPiece
        :return: Lista de tuplas (x, y) con posiciones factibles.
        :rtype: list[tuple[float, float]]
        """
        feasible = []
        minx, miny, maxx, maxy = frame.polygon.bounds
        for x in range(int(minx), int(maxx)):
            for y in range(int(miny), int(maxy)):
                candidate = moving_piece.move(x, y)
                if not frame.contains(candidate):
                    continue

                overlap = False
                for placed in placed_pieces:
                    if candidate.polygon.intersects(placed.polygon):
                        overlap = True
                        break

                if not overlap:
                    feasible.append((x, y))

        return feasible

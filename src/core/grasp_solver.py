import random
from src.models import Frame, Placement, PolygonPiece
from .nfp import NFPComputer

class GraspSolver:
    """
    Implementa el algoritmo GRASP para la colocación de piezas poligonales en marcos rectangulares,
    utilizando el cálculo de NFP (No-Fit Polygon) para encontrar posiciones factibles.

    :var frames: Lista de marcos disponibles para colocar las piezas.
    :vartype frames: list[Frame]
    :var pieces: Lista de piezas poligonales a colocar.
    :vartype pieces: list[PolygonPiece]
    :var iterations: Número de iteraciones para la búsqueda GRASP.
    :vartype iterations: int
    """

    def __init__(
        self, frames: list[Frame], pieces: list[PolygonPiece], iterations: int = 10, rcl_size: int = 3
    ):
        """
        Inicializa el solucionador GRASP.

        :param frames: Lista de marcos disponibles.
        :type frames: list[Frame]
        :param pieces: Lista de piezas a colocar.
        :type pieces: list[PolygonPiece]
        :param iterations: Número de iteraciones GRASP. Por defecto es 10.
        :type iterations: int, optional
        :param rcl_size: Tamaño de la lista restringida de candidatos (RCL). Por defecto es 3.
        :type rcl_size: int, optional
        """
        self.frames = frames
        self.pieces = pieces
        self.iterations = iterations
        self.rcl_size = rcl_size

    def solve(self):
        """
        Ejecuta el algoritmo GRASP para encontrar la mejor distribución de piezas en los marcos.
        Intenta colocar la mayor cantidad de piezas posible, minimizando el desperdicio.

        :return: Diccionario con la lista de colocaciones óptimas y la lista de piezas no colocadas.
        :rtype: dict{'placements': list[Placement], 'not_placed': list[PolygonPiece], 'waste': float}
        """
        best_solution = None
        best_not_placed = None
        best_waste = float("inf")
        best_placed_count = -1

        for _ in range(self.iterations):
            pieces_left = self.pieces[:]
            placements = []
            used_frames = [frame.copy() for frame in self.frames]
            not_placed = []

            while pieces_left:
                # Ordena por área descendente y toma las N más grandes como candidatos (RCL)
                pieces_sorted = sorted(pieces_left, key=lambda p: p.polygon.area, reverse=True)
                rcl = pieces_sorted[:self.rcl_size] if len(pieces_sorted) >= self.rcl_size else pieces_sorted
                piece = random.choice(rcl)
                pieces_left.remove(piece)

                placed = False
                for frame in used_frames:
                    pos = self.find_feasible_position_nfp(frame, placements, piece)
                    if pos:
                        moved_piece = piece.move(*pos)
                        placements.append(Placement(moved_piece, frame, pos))
                        placed = True
                        break

                if not placed:
                    not_placed.append(piece)

            waste = sum(frame.polygon.area for frame in used_frames) - sum(
                p.piece.polygon.area for p in placements
            )
            placed_count = len(placements)

            # Prioriza la mayor cantidad de piezas colocadas, luego el menor desperdicio
            if (placed_count > best_placed_count) or (
                placed_count == best_placed_count and waste < best_waste
            ):
                best_solution = placements
                best_not_placed = not_placed
                best_waste = waste
                best_placed_count = placed_count

        return {
            "placements": best_solution,
            "not_placed": best_not_placed,
            "waste": best_waste,
        }

    def find_feasible_position_nfp(self, frame: Frame, placements: list[Placement], piece: PolygonPiece):
        """
        Busca una posición factible para la pieza en el marco usando NFP.

        :param frame: Marco donde se intenta colocar la pieza.
        :type frame: Frame
        :param placements: Lista de piezas ya colocadas.
        :type placements: list[Placement]
        :param piece: Pieza a colocar.
        :type piece: PolygonPiece
        :return: Coordenadas (x, y) de la posición factible, o None si no hay.
        :rtype: tuple[float, float] or None
        """
        # Comienza con el área disponible igual al marco
        available_region = frame.polygon

        # Resta las piezas ya colocadas en este marco del área disponible
        for p in placements:
            if p.frame == frame:
                available_region = available_region.difference(p.piece.polygon)

        # Si no hay piezas colocadas aún, usar la esquina inferior izquierda del marco
        if not any(p.frame == frame for p in placements):
            minx, miny, _, _ = available_region.bounds
            return (minx, miny)

        # Calcula los NFP para todas las piezas ya colocadas en este marco
        nfp_union = None
        for p in placements:
            if p.frame == frame:
                nfp = NFPComputer.compute_nfp(p.piece.polygon, piece.polygon)
                nfp = nfp.intersection(available_region)
                if nfp_union is None:
                    nfp_union = nfp
                else:
                    nfp_union = nfp_union.union(nfp)

        # La región factible es la intersección entre el área disponible y la unión de los NFP
        feasible_region = (
            available_region
            if nfp_union is None
            else available_region.intersection(nfp_union)
        )

        # Si no hay región factible, retorna None
        if feasible_region.is_empty:
            return None

        # Si la región factible es un polígono o multipolígono, busca el punto más bajo
        if feasible_region.geom_type == "Polygon":
            minx, miny, _, _ = feasible_region.bounds
            return (minx, miny)
        elif feasible_region.geom_type == "MultiPolygon":
            # Elige el polígono con el menor miny, luego menor minx
            min_point = None
            for poly in feasible_region.geoms:
                x, y, _, _ = poly.bounds
                if (
                    (min_point is None)
                    or (y < min_point[1])
                    or (y == min_point[1] and x < min_point[0])
                ):
                    min_point = (x, y)

            return min_point

import random
from src.models import Frame, Placement, PolygonPiece
from .nfp import NFPComputer
from shapely.geometry import Point

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

    def __init__(self, pieces: list[PolygonPiece], frames: list[Frame], iterations: int = 10, rcl_size: int = 3):
        """
        Inicializa el solver GRASP para el problema de colocación de piezas poligonales.

        :param pieces: Lista de piezas poligonales a colocar
        :param frames: Lista de marcos rectangulares donde colocar las piezas
        :param iterations: Número de iteraciones del algoritmo GRASP
        :param rcl_size: Tamaño de la lista restringida de candidatos (RCL)
        """
        self.pieces = pieces
        self.frames = frames
        self.iterations = iterations
        self.rcl_size = rcl_size

    def solve(self):
        """
        Ejecuta el algoritmo GRASP para encontrar la mejor distribución de piezas en los marcos.
        """
        best_solution = None
        best_not_placed = None
        best_waste = float("inf")
        best_placed_count = -1

        for _ in range(self.iterations):
            pieces_left = self.pieces[:]  # Usar una copia de la lista, no de los objetos
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
                    # Intentar colocar la pieza en diferentes posiciones
                    for attempt in range(5):  # Intentar hasta 5 veces con diferentes posiciones
                        pos = self.find_feasible_position_nfp(frame, placements, piece)
                        if pos:
                            moved_piece = piece.move(*pos)
                            # Verificar que no hay solapamiento
                            if not any(moved_piece.polygon.intersects(p.piece.polygon) for p in placements):
                                placements.append(Placement(moved_piece, frame, pos))
                                placed = True
                                break
                        if placed:
                            break
                    if placed:
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
        """
        # Si no hay piezas colocadas aún, usar la esquina inferior izquierda del marco
        if not any(p.frame == frame for p in placements):
            minx, miny, _, _ = frame.polygon.bounds
            return (minx, miny)

        # Comienza con el área disponible igual al marco
        available_region = frame.polygon

        # Calcula los NFP para todas las piezas ya colocadas en este marco
        nfp_union = None
        for p in placements:
            if p.frame == frame:
                nfp = NFPComputer.compute_nfp(p.piece, piece)
                if nfp_union is None:
                    nfp_union = nfp
                else:
                    nfp_union = nfp_union.union(nfp)

        # La región factible es el área disponible menos la unión de los NFP
        if nfp_union:
            feasible_region = available_region.difference(nfp_union)
        else:
            feasible_region = available_region

        # Si no hay región factible, retorna None
        if feasible_region.is_empty:
            return None

        # Buscar una posición factible en la región
        if feasible_region.geom_type == "Polygon":
            # Intentar diferentes puntos dentro del polígono
            minx, miny, maxx, maxy = feasible_region.bounds
            for x in range(int(minx), int(maxx), 2):  # Paso de 2 para reducir el número de intentos
                for y in range(int(miny), int(maxy), 2):
                    point = (x, y)
                    if feasible_region.contains(Point(point)):
                        test_piece = piece.move(x, y)
                        if frame.contains(test_piece) and not any(
                            test_piece.polygon.intersects(p.piece.polygon) for p in placements if p.frame == frame
                        ):
                            return point
        elif feasible_region.geom_type == "MultiPolygon":
            # Intentar en cada polígono de la región factible
            for poly in feasible_region.geoms:
                minx, miny, maxx, maxy = poly.bounds
                for x in range(int(minx), int(maxx), 2):
                    for y in range(int(miny), int(maxy), 2):
                        point = (x, y)
                        if poly.contains(Point(point)):
                            test_piece = piece.move(x, y)
                            if frame.contains(test_piece) and not any(
                                test_piece.polygon.intersects(p.piece.polygon) for p in placements if p.frame == frame
                            ):
                                return point

        return None

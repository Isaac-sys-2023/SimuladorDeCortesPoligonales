import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from shapely.affinity import translate

from src.models import Frame, Placement, PolygonPiece


class PlacementVisualizer:
    """
    Clase para visualizar gráficamente los resultados de la colocación de piezas en los marcos.

    :var frames: Lista de marcos utilizados.
    :type frames: list[Frame]
    :var placements: Lista de colocaciones realizadas.
    :type placements: list[Placement]
    :var not_placed: Lista de piezas no colocadas.
    :type not_placed: list[PolygonPiece]
    :var waste: Área total desperdiciada.
    :type waste: float
    """

    def __init__(
        self,
        frames: list[Frame],
        placements: list[Placement],
        not_placed: list[PolygonPiece],
        waste: float,
    ):
        """
        Inicializa el visualizador con los datos de colocación.
        :param frames: Lista de marcos utilizados.
        :type frames: list[Frame]
        :param placements: Lista de colocaciones realizadas.
        :type placements: list[Placement]
        :param not_placed: Lista de piezas no colocadas.
        :type not_placed: list[PolygonPiece]
        :param waste: Área total desperdiciada.
        :type waste: float
        """
        self.frames = frames
        self.placements = placements
        self.not_placed = not_placed
        self.waste = waste

    def show(self):
        """
        Muestra una visualización gráfica de los marcos, las piezas colocadas y las no colocadas.
        """
        fig, ax = plt.subplots()
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

        # Dibujar marcos
        for idx, frame in enumerate(self.frames):
            x, y = frame.polygon.exterior.xy
            ax.plot(
                x,
                y,
                color="black",
                linewidth=2,
                label=f"Marco {idx+1}" if idx == 0 else "",
            )

        # Dibujar piezas colocadas
        for i, placement in enumerate(self.placements):
            poly = placement.piece.polygon
            patch = MplPolygon(
                list(poly.exterior.coords),
                closed=True,
                facecolor=colors[i % len(colors)],
                alpha=0.6,
                edgecolor="black",
                label=None,
            )
            ax.add_patch(patch)
            # Etiqueta con el nombre de la pieza
            centroid = poly.centroid
            ax.text(
                centroid.x,
                centroid.y,
                placement.piece.name,
                fontsize=8,
                ha="center",
                va="center",
                color="black",
            )

        # Dibujar piezas no colocadas (en una esquina)
        if self.not_placed:
            offset_x = max([frame.polygon.bounds[2] for frame in self.frames]) + 10
            offset_y = 0
            for i, piece in enumerate(self.not_placed):
                poly = piece.polygon
                moved_poly = translate(poly, xoff=offset_x, yoff=offset_y)
                patch = MplPolygon(
                    list(moved_poly.exterior.coords),
                    closed=True,
                    facecolor="none",
                    edgecolor="red",
                    linestyle="--",
                    label="No colocada" if i == 0 else "",
                )
                ax.add_patch(patch)
                centroid = moved_poly.centroid
                ax.text(
                    centroid.x,
                    centroid.y,
                    piece.name,
                    fontsize=8,
                    ha="center",
                    va="center",
                    color="red",
                )
                offset_y += poly.bounds[3] - poly.bounds[1] + 5  # Espaciado

        # Mostrar desperdicio
        ax.set_title(f"Colocación de piezas - Desperdicio: {self.waste:.2f} unidades²")
        ax.set_aspect("equal")
        ax.legend(loc="upper right")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

    def visualize(self, fig):
        """
        Visualiza la colocación en una figura de matplotlib.
        
        :param fig: Figura de matplotlib donde dibujar
        :type fig: matplotlib.figure.Figure
        """
        ax = fig.add_subplot(111)
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

        # Dibujar marcos
        for idx, frame in enumerate(self.frames):
            x, y = frame.polygon.exterior.xy
            ax.plot(
                x,
                y,
                color="black",
                linewidth=2,
                label=f"Marco {idx+1}" if idx == 0 else "",
            )

        # Dibujar piezas colocadas
        for i, placement in enumerate(self.placements):
            poly = placement.piece.polygon
            patch = MplPolygon(
                list(poly.exterior.coords),
                closed=True,
                facecolor=colors[i % len(colors)],
                alpha=0.6,
                edgecolor="black",
                label=None,
            )
            ax.add_patch(patch)
            # Etiqueta con el nombre de la pieza
            centroid = poly.centroid
            ax.text(
                centroid.x,
                centroid.y,
                placement.piece.name,
                fontsize=8,
                ha="center",
                va="center",
                color="black",
            )

        # Dibujar piezas no colocadas (en una esquina)
        if self.not_placed:
            offset_x = max([frame.polygon.bounds[2] for frame in self.frames]) + 10
            offset_y = 0
            for i, piece in enumerate(self.not_placed):
                poly = piece.polygon
                moved_poly = translate(poly, xoff=offset_x, yoff=offset_y)
                patch = MplPolygon(
                    list(moved_poly.exterior.coords),
                    closed=True,
                    facecolor="none",
                    edgecolor="red",
                    linestyle="--",
                    label="No colocada" if i == 0 else "",
                )
                ax.add_patch(patch)
                centroid = moved_poly.centroid
                ax.text(
                    centroid.x,
                    centroid.y,
                    piece.name,
                    fontsize=8,
                    ha="center",
                    va="center",
                    color="red",
                )
                offset_y += poly.bounds[3] - poly.bounds[1] + 5  # Espaciado

        # Mostrar desperdicio
        ax.set_title(f"Colocación de piezas - Desperdicio: {self.waste:.2f} unidades²")
        ax.set_aspect("equal")
        ax.legend(loc="upper right")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

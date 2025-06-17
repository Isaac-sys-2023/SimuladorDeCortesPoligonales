from src.models import Frame, PolygonPiece
from src.core.grasp_solver import GraspSolver
from src.core.placement_visualizer import PlacementVisualizer


def shape_to_verts(name):
    shapes = {
        "rectangulo": [(10, 10), (70, 10), (70, 40), (10, 40)],
        "cuadrado": [(10, 10), (50, 10), (50, 50), (10, 50)],
        "triangulo": [(30, 5), (55, 50), (5, 50)],
        "pentagono": [(30, 5), (60, 20), (50, 50), (10, 50), (0, 20)],
        "hexagono": [(20, 5), (60, 5), (75, 30), (60, 55), (20, 55), (5, 30)],
        "rombo": [(30, 5), (55, 30), (30, 55), (5, 30)],
        "punta": [(30, 5), (60, 15), (30, 25), (0, 15)],
        "trapecio": [(20, 10), (50, 10), (60, 50), (10, 50)],
        "trapezoide": [(10, 10), (60, 10), (50, 50), (20, 50)],
        "trapecio_inclinado": [(10, 10), (70, 10), (60, 50), (0, 50)],
        "escalera": [(10, 10), (40, 10), (40, 25), (70, 25), (70, 50), (10, 50)],
        "figura_L": [(10, 10), (30, 10), (30, 40), (60, 40), (60, 60), (10, 60)]
    }
    return shapes.get(name, [])

def main():
    # Crear un marco de ejemplo
    frame = Frame(width=100, height=60)

    # Usar algunas figuras predeterminadas como piezas
    piece_names = ["rectangulo", "cuadrado", "triangulo", "pentagono", "hexagono"]
    pieces = []
    for name in piece_names:
        vertices = shape_to_verts(name)
        if vertices:
            # Normaliza y escala a un tamaño arbitrario para la simulación
            piece = PolygonPiece(name=name, vertices=vertices)
            piece.scale_to_unit()
            piece.scale_to_size(20, 20)  # Por ejemplo, escalar a 20x20
            pieces.append(piece)

    # Ejecutar el solver GRASP
    solver = GraspSolver(frames=[frame], pieces=pieces, iterations=20)
    result = solver.solve()

    # Visualizar resultados
    visualizer = PlacementVisualizer(
        frames=[frame],
        placements=result["placements"],
        not_placed=result["not_placed"],
        waste=result["waste"],
    )
    visualizer.show()


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.core.grasp_solver import GraspSolver
from src.models import Frame, PolygonPiece
from src.core.placement_visualizer import PlacementVisualizer

# Lista global para almacenar las piezas añadidas al sistema
figuras_en_sistema = []

def cordenada_forma(name):
    """
    Retorna las coordenadas de los vértices para cada tipo de figura predeterminada.
    Las coordenadas están normalizadas para que todas las figuras tengan un tamaño similar.
    
    :param name: Nombre de la figura
    :type name: str
    :return: Lista de tuplas (x,y) representando los vértices de la figura
    :rtype: list[tuple[float, float]]
    """
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

def agregar_figura_sistema(nombre, ancho=None, alto=None):
    """
    Agrega una nueva pieza al sistema con las dimensiones especificadas.
    Si no se proporcionan dimensiones, se usa un tamaño por defecto.
    
    :param nombre: Nombre de la figura
    :type nombre: str
    :param ancho: Ancho de la pieza
    :type ancho: float, optional
    :param alto: Alto de la pieza
    :type alto: float, optional
    """
    coords = cordenada_forma(nombre)
    if coords:
        # Crear la pieza con las coordenadas
        pieza = PolygonPiece(nombre, coords)
        
        # Escalar la pieza si se proporcionaron dimensiones
        if ancho is not None and alto is not None:
            pieza.scale_to_size(float(ancho), float(alto))
        else:
            pieza.scale_to_size(8, 8)  # Tamaño por defecto
        
        figuras_en_sistema.append(pieza)
        actualizar_lista_piezas()

def crear_label_figura(parent, nombre):
    """
    Crea un widget que muestra una figura predeterminada con su nombre.
    Al hacer clic en el widget se abre la ventana para ingresar las dimensiones.
    
    :param parent: Widget padre donde se creará el label
    :type parent: tk.Widget
    :param nombre: Nombre de la figura
    :type nombre: str
    """
    frame = tk.Frame(parent, bd=1, relief="solid", padx=5, pady=5)
    frame.pack(pady=5)

    label = tk.Label(frame, text=nombre)
    label.pack()
    
    canvas = tk.Canvas(frame, width=80, height=80)
    canvas.pack()
    dibujar_figura(canvas, nombre)

    # Vincular eventos de clic para abrir la ventana de datos
    frame.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))
    label.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))
    canvas.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))

def abrir_ventana_datos(nombre_figura):
    """
    Abre una ventana para ingresar las dimensiones específicas de la figura seleccionada.
    Los campos mostrados dependen del tipo de figura.
    
    :param nombre_figura: Nombre de la figura seleccionada
    :type nombre_figura: str
    """
    ventana = tk.Toplevel()
    ventana.title(f"Datos para {nombre_figura}")
    ventana.geometry("250x200")

    entradas = {}

    def agregar_campo(campo):
        """
        Agrega un campo de entrada para una dimensión específica.
        
        :param campo: Nombre del campo
        :type campo: str
        """
        tk.Label(ventana, text=f"{campo.capitalize()}:").pack()
        entrada = tk.Entry(ventana)
        entrada.pack()
        entradas[campo] = entrada

    # Campos específicos según la figura
    if nombre_figura == "cuadrado":
        agregar_campo("lado")
    elif nombre_figura == "rectangulo":
        agregar_campo("base")
        agregar_campo("altura")
    elif nombre_figura == "triangulo":
        agregar_campo("base")
        agregar_campo("altura")
    elif nombre_figura in ["pentagono", "hexagono"]:
        agregar_campo("lado")
    elif nombre_figura == "rombo":
        agregar_campo("diagonal mayor")
        agregar_campo("diagonal menor")
    elif nombre_figura == "trapecio":
        agregar_campo("base mayor")
        agregar_campo("base menor")
        agregar_campo("altura")
    elif nombre_figura == "trapezoide":
        agregar_campo("base mayor")
        agregar_campo("base menor")
        agregar_campo("altura")
    elif nombre_figura == "trapecio_inclinado":
        agregar_campo("base mayor")
        agregar_campo("base menor")
        agregar_campo("altura")
    elif nombre_figura == "escalera":
        agregar_campo("altura total")
        agregar_campo("ancho total")
        agregar_campo("altura grada")
        agregar_campo("ancho grada")
    elif nombre_figura == "figura_L":
        agregar_campo("ancho brazo")
        agregar_campo("alto brazo")
        agregar_campo("ancho base")
    elif nombre_figura == "punta":
        agregar_campo("base")
        agregar_campo("altura")

    def calcular_dimensiones():
        """
        Calcula las dimensiones finales de la pieza basándose en los parámetros ingresados
        y agrega la pieza al sistema.
        """
        try:
            if nombre_figura == "cuadrado":
                lado = float(entradas["lado"].get())
                ancho = alto = lado
            elif nombre_figura == "rectangulo":
                ancho = float(entradas["base"].get())
                alto = float(entradas["altura"].get())
            elif nombre_figura == "triangulo":
                ancho = float(entradas["base"].get())
                alto = float(entradas["altura"].get())
            elif nombre_figura == "pentagono":
                lado = float(entradas["lado"].get())
                # Aproximación para pentágono regular
                ancho = alto = lado * 1.7
            elif nombre_figura == "hexagono":
                lado = float(entradas["lado"].get())
                # Aproximación para hexágono regular
                ancho = lado * 2
                alto = lado * 1.73
            elif nombre_figura == "rombo":
                d1 = float(entradas["diagonal mayor"].get())
                d2 = float(entradas["diagonal menor"].get())
                ancho = d1
                alto = d2
            elif nombre_figura in ["trapecio", "trapezoide", "trapecio_inclinado"]:
                b1 = float(entradas["base mayor"].get())
                b2 = float(entradas["base menor"].get())
                h = float(entradas["altura"].get())
                ancho = max(b1, b2)
                alto = h
            elif nombre_figura == "escalera":
                ancho = float(entradas["ancho total"].get())
                alto = float(entradas["altura total"].get())
            elif nombre_figura == "figura_L":
                ancho = float(entradas["ancho brazo"].get()) + float(entradas["ancho base"].get())
                alto = float(entradas["alto brazo"].get())
            elif nombre_figura == "punta":
                ancho = float(entradas["base"].get())
                alto = float(entradas["altura"].get())

            agregar_figura_sistema(nombre_figura, ancho, alto)
            ventana.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")

    tk.Button(ventana, text="Aceptar", command=calcular_dimensiones).pack(pady=10)

def dibujar_figura(canvas, nombre):
    """
    Dibuja una figura en el canvas especificado.
    
    :param canvas: Canvas donde se dibujará la figura
    :type canvas: tk.Canvas
    :param nombre: Nombre de la figura a dibujar
    :type nombre: str
    """
    coords = cordenada_forma(nombre)
    if coords:
        canvas.create_polygon(coords, outline="black", fill="")

def actualizar_lista_piezas():
    """
    Muestra las piezas con su nombre, área y dibujo a color en el panel 'Piezas del sistema'.
    """
    colores = [
        "#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CCCCFF", "#FFD699",
        "#E0B0FF", "#F7BE81", "#82CAFA", "#FFB6C1", "#B0E0E6", "#C3FDB8"
    ]

    for widget in frame_lista_piezas.winfo_children():
        widget.destroy()

    for i, pieza in enumerate(figuras_en_sistema):
        color = colores[i % len(colores)]

        contenedor = tk.Frame(frame_lista_piezas, bd=1, relief="solid", padx=4, pady=2)
        contenedor.pack(fill="x", pady=3)

        # Dibujo de la figura
        canvas = tk.Canvas(contenedor, width=80, height=60, bg="white")
        canvas.pack(side="left", padx=4)

        # Obtener coordenadas normalizadas al canvas
        coords = pieza.polygon.exterior.coords
        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)
        max_x = max(x for x, y in coords)
        max_y = max(y for x, y in coords)
        scale = min(60 / (max_x - min_x + 1e-5), 50 / (max_y - min_y + 1e-5))

        desplazada = [
            ((x - min_x) * scale + 10, (y - min_y) * scale + 5)
            for x, y in coords
        ]

        canvas.create_polygon(desplazada, fill=color, outline="black")

        # Info textual y botón
        info_frame = tk.Frame(contenedor)
        info_frame.pack(side="left", fill="both", expand=True)

        tk.Label(info_frame, text=f"Pieza {i+1}: {pieza.name}", font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(info_frame, text=f"Área: {pieza.polygon.area:.2f}", font=("Arial", 8)).pack(anchor="w")

        def eliminar(idx=i):
            confirm = messagebox.askyesno("Eliminar", f"¿Eliminar pieza {idx+1} ({pieza.name})?")
            if confirm:
                del figuras_en_sistema[idx]
                actualizar_lista_piezas()

        tk.Button(info_frame, text="❌", command=eliminar, fg="red", font=("Arial", 8)).pack(anchor="e", pady=2)



def simular():
    """
    Ejecuta la simulación de colocación de piezas usando el algoritmo GRASP.
    Muestra los resultados en el gráfico y actualiza la información de resultados.
    """
    if not figuras_en_sistema:
        messagebox.showwarning("Advertencia", "No hay piezas para simular")
        return

    try:
        # Crear el marco con las dimensiones correctas
        try:
            base = float(entry_base.get())
            altura = float(entry_altura.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos para base y altura.")
            return

        frame = Frame(base, altura)
        solver = GraspSolver(pieces=figuras_en_sistema, frames=[frame])
        result = solver.solve()

        if result["placements"]:
            for widget in frame_grafico.winfo_children():
                widget.destroy()

            fig = plt.Figure(figsize=(6, 6))
            canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
            canvas.get_tk_widget().pack(fill="both", expand=True)

            visualizer = PlacementVisualizer(
                frames=[frame],
                placements=result["placements"],
                not_placed=result["not_placed"],
                waste=result["waste"]
            )
            visualizer.visualize(fig)
            canvas.draw()

            for widget in frame_resultados.winfo_children():
                widget.destroy()

            tk.Label(frame_resultados, text="Resultados", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(frame_resultados, text=f"Piezas colocadas: {len(result['placements'])}").pack()
            tk.Label(frame_resultados, text=f"Piezas no colocadas: {len(result['not_placed'])}").pack()
            tk.Label(frame_resultados, text=f"Área desperdiciada: {result['waste']:.2f}").pack()
            tk.Label(frame_resultados, text=f"Área total: {(base * altura):.2f}").pack()
            tk.Label(frame_resultados, text=f"Porcentaje de aprovechamiento: {((1 - (result['waste'] / (base * altura)))*100):.2f} %").pack()
        else:
            messagebox.showinfo("Resultado", "No se pudo colocar ninguna pieza")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la simulación: {str(e)}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Sistema de Corte de Piezas")
root.geometry("1200x600")

# Panel de gráfico
frame_grafico = tk.Frame(root, width=600, height=600, bd=2, relief="groove")
frame_grafico.pack(side="left", fill="both", expand=True)

# Panel de resultados
frame_resultados = tk.Frame(root, width=150, bd=2, relief="groove")
frame_resultados.pack(side="left", fill="y")
tk.Label(frame_resultados, text="Resultados", font=("Arial", 12, "bold")).pack(pady=10)

# Panel de piezas del sistema
frame_sistema = tk.Frame(root, width=150, bd=2, relief="groove")
frame_sistema.pack(side="left", fill="y")
tk.Label(frame_sistema, text="Piezas del sistema", font=("Arial", 10)).pack()

# Lista de piezas
frame_lista_piezas = tk.Frame(frame_sistema)
frame_lista_piezas.pack(fill="both", expand=True)

# Panel de figuras predeterminadas
frame_predet = tk.Frame(root, width=160, bd=2, relief="groove")
frame_predet.pack(side="left", fill="y")

tk.Label(frame_predet, text="Figuras predeterminadas", font=("Arial", 10)).pack()

# Configuración del scroll para las figuras predeterminadas
canvas_scroll = tk.Canvas(frame_predet, width=150, height=500)
scrollbar = tk.Scrollbar(frame_predet, orient="vertical", command=canvas_scroll.yview)
scrollable_frame = tk.Frame(canvas_scroll)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_scroll.configure(
        scrollregion=canvas_scroll.bbox("all")
    )
)

canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_scroll.configure(yscrollcommand=scrollbar.set)

canvas_scroll.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Panel de configuración para dimensiones de la plancha
config_frame = tk.Frame(root, width=150, bd=2, relief="groove")
config_frame.pack(side="left", fill="y")
tk.Label(config_frame, text="Configurar plancha", font=("Arial", 10)).pack(pady=10)

# Entradas para tamaño de la plancha
tk.Label(config_frame, text="Base de la plancha:").pack()
entry_base = tk.Entry(config_frame)
entry_base.pack()

tk.Label(config_frame, text="Altura de la plancha:").pack()
entry_altura = tk.Entry(config_frame)
entry_altura.pack()



# Botón de simulación
btn_simular = tk.Button(frame_sistema, text="Simular", command=simular)
btn_simular.pack(pady=10)

# Lista de figuras predeterminadas disponibles
figuras = [
    "rectangulo", "cuadrado", "triangulo", "pentagono", "hexagono",
    "rombo", "punta","trapecio", "trapezoide",
    "trapecio_inclinado", "escalera","figura_L"
]

# Crear los widgets para cada figura predeterminada
for fig in figuras:
    crear_label_figura(scrollable_frame, fig)

# Iniciar la aplicación
root.mainloop()

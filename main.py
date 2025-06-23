import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.core.grasp_solver import GraspSolver
from src.models import Frame, PolygonPiece
from src.core.placement_visualizer import PlacementVisualizer
import json


from openpyxl import Workbook
from tkinter import filedialog

# Lista global para almacenar las piezas añadidas al sistema
figuras_en_sistema = []

# Variables globales para múltiples planchas
planchas = []  # Lista de frames (plancha)
resultados_planchas = []  # Lista de resultados por plancha
indice_plancha_actual = 0  # Índice de la plancha mostrada

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
    Valida que la pieza no sea más grande que la plancha definida por el usuario.
    Asigna un identificador único (pieza 1, pieza 2, ...) a cada pieza.
    """
    coords = cordenada_forma(nombre)
    if coords:
        pieza = PolygonPiece(nombre, coords)
        # Obtener dimensiones actuales de la plancha
        try:
            base_plancha = float(entry_base.get())
            altura_plancha = float(entry_altura.get())
        except Exception:
            base_plancha = None
            altura_plancha = None
        if ancho is not None and alto is not None and base_plancha and altura_plancha:
            if float(ancho) > base_plancha or float(alto) > altura_plancha:
                messagebox.showerror("Error", f"La pieza es más grande que la plancha ({base_plancha}x{altura_plancha}) y no puede ser agregada.")
                return
            pieza.scale_to_size(float(ancho), float(alto))
        else:
            pieza.scale_to_size(8, 8)
        # Asignar identificador único
        pieza.etiqueta = f"pieza {len(figuras_en_sistema)+1}"
        figuras_en_sistema.append(pieza)
        actualizar_lista_piezas()

def crear_label_figura(parent, nombre, color):
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
    dibujar_figura(canvas, nombre, color)

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

def guardar_json():
    datos = {
        "plancha": {
            "base": float(entry_base.get()),
            "altura": float(entry_altura.get())
        },
        "piezas": [
            {
                "nombre": pieza.name,
                "ancho": pieza.polygon.bounds[2] - pieza.polygon.bounds[0],
                "alto": pieza.polygon.bounds[3] - pieza.polygon.bounds[1],
                "area": pieza.polygon.area
            }
            for pieza in figuras_en_sistema
        ]
    }
    archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if archivo:
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
        messagebox.showinfo("Éxito", "Datos guardados en JSON.")

def cargar_json():
    archivo = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not archivo:
        return
    try:
        with open(archivo, "r") as f:
            datos = json.load(f)
        
        # Cargar plancha
        entry_base.delete(0, tk.END)
        entry_base.insert(0, datos["plancha"]["base"])
        entry_altura.delete(0, tk.END)
        entry_altura.insert(0, datos["plancha"]["altura"])

        # Cargar piezas
        figuras_en_sistema.clear()
        for pieza_data in datos["piezas"]:
            agregar_figura_sistema(
                pieza_data["nombre"],
                pieza_data["ancho"],
                pieza_data["alto"]
            )
        actualizar_lista_piezas()
        messagebox.showinfo("Éxito", "Datos cargados desde JSON.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

def dibujar_figura(canvas, nombre, color):
    """
    Dibuja una figura en el canvas especificado.
    
    :param canvas: Canvas donde se dibujará la figura
    :type canvas: tk.Canvas
    :param nombre: Nombre de la figura a dibujar
    :type nombre: str
    """
    coords = cordenada_forma(nombre)
    if coords:
        canvas.create_polygon(coords, outline="black", fill=color)

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
    Ahora soporta múltiples planchas: si una pieza no cabe en la plancha actual,
    se crea una nueva plancha y se intenta colocar ahí solo las piezas no colocadas.
    La visualización permite navegar entre planchas generadas.
    """
    global planchas, resultados_planchas, indice_plancha_actual
    if not figuras_en_sistema:
        messagebox.showwarning("Advertencia", "No hay piezas para simular")
        return

    try:
        # Obtener dimensiones de la plancha ingresadas por el usuario
        try:
            base = float(entry_base.get())
            altura = float(entry_altura.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos para base y altura de la plancha.")
            return

        # Inicializar variables para el manejo de múltiples planchas
        piezas_restantes = figuras_en_sistema[:]  # Copia de las piezas a colocar
        planchas = []  # Lista de frames (una por cada plancha usada)
        resultados_planchas = []  # Resultados de la simulación por plancha
        indice_plancha_actual = 0  # Índice de la plancha mostrada

        # Límite de iteraciones para evitar bucles infinitos
        max_iter = len(piezas_restantes)
        iter_count = 0
        while piezas_restantes and iter_count < max_iter:
            # Crear una nueva plancha con las dimensiones del usuario
            frame = Frame(base, altura)
            # Solo se intentan colocar las piezas que no han sido colocadas en planchas anteriores
            solver = GraspSolver(pieces=piezas_restantes, frames=[frame])
            result = solver.solve()
            planchas.append(frame)
            resultados_planchas.append(result)
            # Solo las piezas no colocadas pasan a la siguiente plancha
            piezas_restantes = result["not_placed"]
            # Si no se pudo colocar ninguna pieza nueva, romper para evitar bucle infinito
            if not result["placements"]:
                break
            iter_count += 1

        # Mostrar la primera plancha si hay resultados
        if resultados_planchas:
            mostrar_plancha(0)
        else:
            messagebox.showinfo("Resultado", "No se pudo colocar ninguna pieza")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la simulación: {str(e)}")

def mostrar_plancha(indice):
    """
    Muestra la visualización y resultados de la plancha en la posición 'indice'.
    Permite navegar entre planchas usando los botones 'Anterior' y 'Siguiente'.
    """
    global indice_plancha_actual
    if not resultados_planchas:
        return
    indice_plancha_actual = indice
    result = resultados_planchas[indice]
    frame = planchas[indice]
    base = frame.width
    altura = frame.height

    # Limpiar el canvas del gráfico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Crear la visualización de la plancha actual
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

    # Actualizar resultados y controles de navegación
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    tk.Label(frame_resultados, text=f"Resultados - Plancha {indice+1} de {len(planchas)}", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(frame_resultados, text=f"Piezas colocadas: {len(result['placements'])}").pack()
    tk.Label(frame_resultados, text=f"Piezas no colocadas: {len(result['not_placed'])}").pack()
    tk.Label(frame_resultados, text=f"Área desperdiciada: {result['waste']:.2f}").pack()
    tk.Label(frame_resultados, text=f"Área total: {(base * altura):.2f}").pack()
    tk.Label(frame_resultados, text=f"Porcentaje de aprovechamiento: {((1 - (result['waste'] / (base * altura)))*100):.2f} %").pack()

    # Botones para navegar entre planchas
    nav_frame = tk.Frame(frame_resultados)
    nav_frame.pack(pady=10)
    btn_prev = tk.Button(nav_frame, text="Anterior", command=lambda: mostrar_plancha(max(0, indice_plancha_actual-1)))
    btn_prev.pack(side="left", padx=5)
    btn_next = tk.Button(nav_frame, text="Siguiente", command=lambda: mostrar_plancha(min(len(planchas)-1, indice_plancha_actual+1)))
    btn_next.pack(side="left", padx=5)
    if indice_plancha_actual == 0:
        btn_prev.config(state="disabled")
    if indice_plancha_actual == len(planchas)-1:
        btn_next.config(state="disabled")

    # Botón de exportar solo para la plancha actual
    tk.Button(
        frame_resultados,
        text="Exportar a Excel",
        command=lambda: exportar_resultados_excel(result, base, altura)
    ).pack(pady=10)

def exportar_resultados_excel(resultados, ancho, alto):
    archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo Excel", "*.xlsx")])
    if not archivo:
        return

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"

        # Resultados resumen
        ws["A1"] = "Piezas Colocadas"
        ws["B1"] = len(resultados["placements"])
        ws["A2"] = "Piezas no colocadas"
        ws["B2"] = len(resultados["not_placed"])
        ws["A3"] = "Área desperdiciada"
        ws["B3"] = round(resultados["waste"], 2)
        ws["A4"] = "Área total"
        ws["B4"] = round(ancho * alto, 2)
        ws["A5"] = "Porcentaje de aprovechamiento"
        ws["B5"] = round((1 - (resultados['waste'] / (ancho * alto)))*100, 2)

        # Dimensiones de la plancha
        ws["D1"] = "Dimensiones de la plancha"
        ws["D2"] = "Base"
        ws["E2"] = ancho
        ws["D3"] = "Altura"
        ws["E3"] = alto

        # Encabezados para detalles de piezas
        ws["G1"] = "Número de Pieza"
        ws["H1"] = "Tipo de Pieza"
        ws["I1"] = "Área de la pieza"

        fila = 2

        print(vars(resultados["placements"][0]))

        # Piezas colocadas
        for idx, pieza in enumerate(figuras_en_sistema, start=1):
            tipo = pieza.name
            area = pieza.polygon.area

            ws.cell(row=fila, column=7, value=f"Pieza {idx}")
            ws.cell(row=fila, column=8, value=tipo)
            ws.cell(row=fila, column=9, value=area)
            
            fila += 1


        wb.save(archivo)
        messagebox.showinfo("Éxito", "Resultados exportados a Excel correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel:\n{str(e)}")

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
tk.Button(config_frame, text="Guardar JSON", command=guardar_json).pack(pady=5)
tk.Button(config_frame, text="Cargar JSON", command=cargar_json).pack(pady=5)

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
colores = [
        "#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CCCCFF", "#FFD699",
        "#E0B0FF", "#F7BE81", "#82CAFA", "#FFB6C1", "#B0E0E6", "#C3FDB8"
    ]

for i, fig in enumerate(figuras):
    color = colores[i % len(colores)]
    crear_label_figura(scrollable_frame, fig, color)

# Iniciar la aplicación
root.mainloop()

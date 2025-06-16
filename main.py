import tkinter as tk
figuras_en_sistema = []
def cordenada_forma(name):
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

def agregar_figura_sistema(nombre):
    coords = cordenada_forma(nombre)
    if coords:
        canvas_sistema.create_polygon(coords, outline="black", fill="")

def crear_label_figura(parent, nombre):
    frame = tk.Frame(parent, bd=1, relief="solid", padx=5, pady=5)
    frame.pack(pady=5)

    label = tk.Label(frame, text=nombre)
    label.pack()
    
    canvas = tk.Canvas(frame, width=80, height=80)
    canvas.pack()
    dibujar_figura(canvas, nombre)

    frame.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))
    label.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))
    canvas.bind("<Button-1>", lambda e: abrir_ventana_datos(nombre))

def abrir_ventana_datos(nombre_figura):
    ventana = tk.Toplevel()
    ventana.title(f"Datos para {nombre_figura}")
    ventana.geometry("250x200")

    entradas = {}

    def agregar_campo(campo):
        tk.Label(ventana, text=f"{campo.capitalize()}:").pack()
        entrada = tk.Entry(ventana)
        entrada.pack()
        entradas[campo] = entrada

    if nombre_figura in ["rectangulo", "trapecio1", "trapecio2"]:
        agregar_campo("base")
        agregar_campo("altura")
    elif nombre_figura == "cuadrado":
        agregar_campo("lado")
    elif nombre_figura == "triangulo":
        agregar_campo("base")
        agregar_campo("altura")
    elif nombre_figura == "pentagono":
        agregar_campo("lado")
    elif nombre_figura == "hexagono":
        agregar_campo("lado")
    elif nombre_figura == "rombo":
        agregar_campo("diagonal mayor")
        agregar_campo("diagonal menor")
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



    #boton
    def aceptar():
        datos = {k: v.get() for k, v in entradas.items()}
        figura_info = {
            "tipo": nombre_figura,
            "parametros": datos
        }
        figuras_en_sistema.append(figura_info)
        ventana.destroy()
    

    tk.Button(ventana, text="Aceptar", command=aceptar).pack(pady=10)

def dibujar_figura(canvas, nombre):
    coords = cordenada_forma(nombre)
    if coords:
        canvas.create_polygon(coords, outline="black", fill="")

#interfaz 
root = tk.Tk()
root.title("Sistema de Corte de Piezas")
root.geometry("1200x600")

#gráfico
frame_grafico = tk.Frame(root, width=600, height=600, bd=2, relief="groove")
frame_grafico.pack(side="left", fill="both", expand=True)
canvas_grafico = tk.Canvas(frame_grafico, bg="white")
canvas_grafico.pack(fill="both", expand=True)
canvas_grafico.create_text(300, 300, text="Gráfico", font=("Arial", 16))

#resultados
frame_resultados = tk.Frame(root, width=150, bd=2, relief="groove")
frame_resultados.pack(side="left", fill="y")
tk.Label(frame_resultados, text="Resultados", font=("Arial", 12, "bold")).pack(pady=10)

#piezas del sistema
frame_sistema = tk.Frame(root, width=150, bd=2, relief="groove")
frame_sistema.pack(side="left", fill="y")
tk.Label(frame_sistema, text="Piezas del sistema", font=("Arial", 10)).pack()
canvas_sistema = tk.Canvas(frame_sistema, width=120, height=400, bg="white")
canvas_sistema.pack()

#predeterminadas
frame_predet = tk.Frame(root, width=160, bd=2, relief="groove")
frame_predet.pack(side="left", fill="y")

tk.Label(frame_predet, text="Figuras predeterminadas", font=("Arial", 10)).pack()

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

figuras = [
    "rectangulo", "cuadrado", "triangulo", "pentagono", "hexagono",
    "rombo", "punta","trapecio", "trapezoide",
    "trapecio_inclinado", "escalera","figura_L"

]

for fig in figuras:
    crear_label_figura(scrollable_frame, fig)


root.mainloop()

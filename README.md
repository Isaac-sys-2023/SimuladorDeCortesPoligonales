# Sistema de Simulación de Corte de Piezas Poligonales

Este sistema implementa un algoritmo GRASP (Greedy Randomized Adaptive Search Procedure) para optimizar la colocación de piezas poligonales en marcos rectangulares, minimizando el área desperdiciada.

## Características principales

- Interfaz gráfica para agregar piezas con dimensiones específicas
- Visualización en tiempo real de las piezas añadidas
- Algoritmo de optimización para la colocación de piezas
- Visualización de resultados con matplotlib
- Cálculo de área desperdiciada y piezas no colocadas

## Requisitos del sistema

- Python 3.8 o superior
- Las librerías listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd SimuladorDeCortesPoligonales
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar el programa principal:
```bash
python main.py
```

2. En la interfaz gráfica:
   - Seleccionar una figura predeterminada del panel izquierdo
   - Ingresar las dimensiones específicas de la figura
   - La pieza se agregará a la lista de piezas del sistema
   - Repetir el proceso para agregar más piezas
   - Presionar "Simular" para ejecutar la optimización

3. Los resultados se mostrarán en:
   - El panel central: visualización gráfica de la colocación
   - El panel derecho: estadísticas de la simulación

## Estructura del proyecto

```
SimuladorDeCortesPoligonales/
├── main.py              # Programa principal
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
└── src/                # Código fuente
    ├── core/           # Implementación de algoritmos
    │   ├── grasp_solver.py
    │   ├── nfp.py
    │   └── placement_visualizer.py
    └── models/         # Modelos de datos
        ├── frame.py
        ├── placement.py
        └── polygon_piece.py
```

## Notas

- El sistema utiliza el algoritmo GRASP para encontrar una solución óptima
- Las piezas se colocan evitando solapamientos usando No-Fit Polygons (NFP)
- El área desperdiciada se calcula como la diferencia entre el área total del marco y el área de las piezas colocadas

## Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Hacer fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request
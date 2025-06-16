# Simulador de cortes poligonales

## Descripción General
El **Simulador de Cortes Poligonales** es una herramienta diseñada para optimizar el corte de piezas (regulares e irregulares) dentro de marcos rectangulares, minimizando el desperdicio de material. Permite al usuario definir los tamaños de los marcos y las piezas, y utiliza algoritmos avanzados como GRASP y NFP para proponer la mejor distribución posible.

## Características
- Interfaz gráfica para ingresar los tamaños de los marcos y las piezas a cortar.
- Soporte para piezas regulares e irregulares, con posibilidad de definir cantidad y dimensiones.
- Algoritmos de optimización (GRASP, NFP y heurísticas) para minimizar el desperdicio.
- Visualización gráfica de los resultados, mostrando la disposición de las piezas, las no colocadas y el área desperdiciada.
- Posibilidad de guardar y cargar configuraciones para pruebas y validaciones futuras.
- Modelos de datos estructurados para marcos y piezas.

## Estructura del Proyecto
```
SimuladorDeCortesPoligonales
├── src
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── core
│   │   ├── grasp_solver.py          # Lógica GRASP y heurísticas de colocación
│   │   ├── nfp.py                   # Cálculo de No-Fit Polygon (NFP)
│   │   ├── placement_visualizer.py  # Visualización de resultados
│   ├── models
│   │   ├── frame.py                 # Modelo de datos para marcos
│   │   ├── placement.py             # Modelo de datos para colocaciones
│   │   └── polygon_piece.py         # Modelo de datos para piezas poligonales
│   └── utils
│       └── helpers.py               # Funciones utilitarias
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Documentación del proyecto
```

## Instalación
1. Clona el repositorio:
   ```
   git clone <url-del-repositorio>
   ```
2. Ingresa al directorio del proyecto:
   ```
   cd SimuladorDeCortesPoligonales
   ```
3. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

## Uso
1. Ejecuta la aplicación:
   ```
   python src/main.py
   ```
2. Utiliza la interfaz gráfica para ingresar los tamaños de los marcos y las piezas (puedes seleccionar figuras predefinidas o cargar tus propias formas).
3. Ejecuta la simulación para obtener la mejor distribución posible, visualiza los resultados y guarda la configuración si lo deseas.

## Pruebas y Validación
- Puedes guardar la configuración de una simulación para repetir pruebas y validar resultados en el futuro.
- El sistema permite cargar configuraciones previas y comparar el desempeño de los algoritmos.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
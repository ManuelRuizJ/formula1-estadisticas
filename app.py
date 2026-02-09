import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# --- Cargar datos acumulados ---
df_pilotos = pd.read_csv("clasificacion_pilotos_acumulado.csv")
df_constructores = pd.read_csv("clasificacion_constructores_acumulado.csv")

# Seleccionar sólo las columnas que corresponden a Grandes Premios.
# Los CSV contienen al final columnas de resumen (ej. Promedio_GP, STD_GP,
# Victories, Podios) que no son GPs y provocan puntos extra en la gráfica.
def get_gp_cols(df):
    cols = list(df.columns)
    # Buscar columna marcador de fin de GPs
    if 'Promedio_GP' in cols:
        end_idx = cols.index('Promedio_GP')
    elif 'Promedio' in cols:
        end_idx = cols.index('Promedio')
    else:
        # Si no existe, tomar todas las columnas desde la 3ª en adelante
        end_idx = len(cols)
    return cols[2:end_idx]

gp_cols_pilotos = get_gp_cols(df_pilotos)       # Columnas de GPs para pilotos
gp_cols_constructores = get_gp_cols(df_constructores)  # Columnas de GPs para constructores

# --- Clase ventana principal ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 - Gráficas Acumuladas")
        self.setGeometry(100, 100, 1200, 800)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QHBoxLayout(self.widget)

        # Panel izquierdo para selección
        self.panel_seleccion = QVBoxLayout()
        self.layout.addLayout(self.panel_seleccion, 1)

        self.tipo_label = QLabel("Selecciona tipo de gráfico:")
        self.panel_seleccion.addWidget(self.tipo_label)

        self.btn_pilotos = QPushButton("Pilotos")
        self.btn_pilotos.clicked.connect(self.mostrar_pilotos)
        self.panel_seleccion.addWidget(self.btn_pilotos)

        self.btn_constructores = QPushButton("Constructores")
        self.btn_constructores.clicked.connect(self.mostrar_constructores)
        self.panel_seleccion.addWidget(self.btn_constructores)

        # Scroll area para checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.panel_seleccion.addWidget(self.scroll_area)

        # Botón para graficar
        self.btn_graficar = QPushButton("Generar gráfica acumulada")
        self.btn_graficar.clicked.connect(self.generar_grafica)
        self.panel_seleccion.addWidget(self.btn_graficar)

        # Área para gráfica
        self.canvas = FigureCanvas(plt.Figure(figsize=(8,6)))
        self.layout.addWidget(self.canvas, 3)

        # Variables
        self.checkboxes = []
        self.tipo = "Pilotos"

        self.mostrar_pilotos()

    # --- Crear checkboxes dinámicos ---
    def mostrar_pilotos(self):
        self.tipo = "Pilotos"
        self.crear_checkboxes(df_pilotos['Piloto'].tolist())

    def mostrar_constructores(self):
        self.tipo = "Constructores"
        self.crear_checkboxes(df_constructores['Escudería'].tolist())

    def crear_checkboxes(self, items):
        # Limpiar scroll anterior
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.checkboxes = []
        for item in items:
            cb = QCheckBox(item)
            cb.setChecked(True)
            self.scroll_layout.addWidget(cb)
            self.checkboxes.append(cb)

    # --- Generar gráfica acumulada ---
    def generar_grafica(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        seleccionados = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        if self.tipo == "Pilotos":
            df = df_pilotos.set_index('Piloto')
            df = df.loc[seleccionados, gp_cols_pilotos]
        else:
            df = df_constructores.set_index('Escudería')
            df = df.loc[seleccionados, gp_cols_constructores]

        # Sumar acumulado
        df_acum = df.cumsum(axis=1)

        # Graficar
        for idx, row in df_acum.iterrows():
            ax.plot(df_acum.columns, row.values, marker='o', label=idx)

        ax.set_title(f"Gráfica acumulada: {self.tipo}")
        ax.set_xlabel("Gran Premio")
        ax.set_ylabel("Puntos acumulados")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, colorchooser
import os
import numpy as np
from matplotlib.lines import Line2D  # Importar para personalizar la leyenda

def leer_bln(ruta_archivo):
    polilineas = []
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    indice = 0
    while indice < len(lineas):
        encabezado = lineas[indice].strip()
        if encabezado:  # Verificar que la línea no esté vacía
            # Suponemos que el encabezado tiene dos números: num_puntos y capa
            # Separados por espacios o comas
            if ',' in encabezado:
                separador = ','
            else:
                separador = None  # None hace que split() use cualquier cantidad de espacios como separador
            partes_encabezado = encabezado.split(separador)
            if len(partes_encabezado) >= 1:
                num_puntos = int(partes_encabezado[0])
                # La capa no es relevante en este caso, así que podemos ignorarla
                indice += 1
                x = []
                y = []
                for _ in range(num_puntos):
                    linea_datos = lineas[indice].strip()
                    if linea_datos:
                        datos = linea_datos.split(separador)
                        if len(datos) >= 2:
                            xi = float(datos[0])
                            yi = float(datos[1])
                            # Ignoramos cualquier dato adicional
                            x.append(xi)
                            y.append(yi)
                        else:
                            raise ValueError(f"Línea de datos con formato incorrecto: {lineas[indice].strip()}")
                    indice += 1
                polilineas.append((x, y))
            else:
                indice += 1
        else:
            indice += 1
    return polilineas

def main():
    # Inicializar Tkinter
    root = tk.Tk()
    root.withdraw()
    
    # Crear figura y ejes
    fig, ax = plt.subplots()
    
    # Seleccionar múltiples archivos a la vez
    rutas_archivos = filedialog.askopenfilenames(
        title="Selecciona uno o más archivos .bln",
        filetypes=[("Archivos BLN", "*.bln")],
        initialdir="."
    )
    
    if rutas_archivos:
        handles = []  # Para almacenar los ítems de la leyenda
        labels = []   # Para almacenar los nombres de los ítems de la leyenda
        
        for ruta_archivo in rutas_archivos:
            polilineas = leer_bln(ruta_archivo)
            nombre_archivo = os.path.splitext(os.path.basename(ruta_archivo))[0]
            
            # Seleccionar color para el archivo actual
            color = colorchooser.askcolor(title=f'Selecciona un color para {nombre_archivo}')[1]
            if not color:
                color = 'black'  # Si el usuario cancela, usar color negro por defecto
            
            for x, y in polilineas:
                # Solo dibujar las polilíneas, sin relleno
                ax.plot(x, y, label=f'{nombre_archivo}', color=color)
            
            # Crear un "handle" con un círculo para la leyenda
            handle = Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
            handles.append(handle)
            labels.append(nombre_archivo)
        
        # Añadir la leyenda personalizada con los círculos
        ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Obtener el valor mínimo y máximo del eje X en los datos
        x_min = min(min(x) for x, y in polilineas)
        x_max = max(max(x) for x, y in polilineas)
        ax.set_xlim([x_min, x_max])
        
        # Ajustar el gráfico
        ax.set_xlabel('Distancia [km]')
        ax.set_ylabel('Profundidad [km]')
        ax.set_title('Corte Diagonal en ...')
        
        # Desactivar la cuadrícula
        ax.grid(False)
        
        # Ajustar el diseño para evitar que el gráfico se superponga con la leyenda
        plt.tight_layout()
        
        # Mostrar el gráfico
        plt.show()
    else:
        print("No se seleccionó ningún archivo.")

if __name__ == "__main__":
    main()

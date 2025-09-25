import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Función para manejar el clic en el botón de aceptar
def aceptar_coordenadas():
    try:
        N1 = float(entry_N1.get())
        E1 = float(entry_E1.get())
        N2 = float(entry_N2.get())
        E2 = float(entry_E2.get())

        # Verificar que las coordenadas ingresadas están dentro del rango de los datos
        if not (N_min <= N1 <= N_max and N_min <= N2 <= N_max and E_min <= E1 <= E_max and E_min <= E2 <= E_max):
            messagebox.showerror("Error", "Las coordenadas están fuera del rango de los datos.")
            return

        # Generar los puntos y continuar con la interpolación
        generar_bln(N1, E1, N2, E2)
        messagebox.showinfo("Éxito", "Archivos BLN generados con éxito.")
        ventana.quit()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese coordenadas numéricas válidas.")

# Función para generar los archivos BLN
def generar_bln(N1, E1, N2, E2):
    # Paso 4: Generar puntos a lo largo de la línea diagonal entre los dos puntos
    num_puntos = 100  # Puedes ajustar este número según tus necesidades
    Ns = np.linspace(N1, N2, num_puntos)
    Es = np.linspace(E1, E2, num_puntos)

    # Calcular la distancia acumulada desde el punto inicial
    distancias = np.sqrt((Ns - N1)**2 + (Es - E1)**2)

    # Paso 5: Interpolar los valores de las capas en los puntos generados
    puntos_datos = data[['N', 'E']].values

    for capa in capas:
        valores_capa = data[capa].values
        try:
            valores_interpolados = griddata(puntos_datos, valores_capa, (Ns, Es), method='linear')
        except Exception as e:
            print(f"Error al interpolar la capa '{capa}': {e}")
            continue

        df_capa = pd.DataFrame({'Distancia': distancias, capa: valores_interpolados})
        df_capa.dropna(inplace=True)
        df_capa.sort_values('Distancia', inplace=True)
        num_puntos_validos = len(df_capa)
        encabezado = f"{num_puntos_validos} 1"
        datos_para_guardar = df_capa[['Distancia', capa]].values
        nombre_archivo = f'{capa}.bln'
        try:
            with open(nombre_archivo, 'w') as f:
                f.write(encabezado + '\n')
                np.savetxt(f, datos_para_guardar, fmt='%.6f', delimiter='\t')
            print(f"Archivo '{nombre_archivo}' generado con éxito.")
        except Exception as e:
            print(f"Error al guardar el archivo '{nombre_archivo}': {e}")

# Inicializar tkinter y ocultar la ventana principal
root = tk.Tk()
root.withdraw()

# Paso 1: Solicitar al usuario que seleccione el archivo de modelo
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo de modelo",
    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
)

if not ruta_archivo:
    messagebox.showerror("Error", "No se seleccionó ningún archivo. El programa se cerrará.")
    exit()

# Leer el archivo y aceptar separadores de espacios o comas
try:
    separador_regex = r'[\s,]+'
    data = pd.read_csv(ruta_archivo, sep=separador_regex, engine='python', header=0)
except Exception as e:
    messagebox.showerror("Error", f"Error al leer el archivo: {e}")
    exit()

# Verificar que el archivo tenga al menos tres columnas
num_columns = data.shape[1]
if num_columns < 3:
    messagebox.showerror("Error", "El archivo debe tener al menos tres columnas.")
    exit()

column_names_original = data.columns.tolist()
data.rename(columns={column_names_original[0]: 'N', column_names_original[1]: 'E'}, inplace=True)
capas = column_names_original[2:]  # Capas a partir de la tercera columna

# Convertir las columnas a numéricas
columnas_numericas = ['N', 'E'] + capas
for col in columnas_numericas:
    data[col] = pd.to_numeric(data[col], errors='coerce')

data.dropna(subset=columnas_numericas, inplace=True)
for capa in capas:
    data[capa] = data[capa].abs()

N_min, N_max = data['N'].min(), data['N'].max()
E_min, E_max = data['E'].min(), data['E'].max()

# Crear la ventana para ingresar las coordenadas
ventana = tk.Tk()
ventana.title("Ingrese las coordenadas UTM")

tk.Label(ventana, text="Coordenada N del punto 1:").grid(row=0, column=0)
entry_N1 = tk.Entry(ventana)
entry_N1.grid(row=0, column=1)

tk.Label(ventana, text="Coordenada E del punto 1:").grid(row=1, column=0)
entry_E1 = tk.Entry(ventana)
entry_E1.grid(row=1, column=1)

tk.Label(ventana, text="Coordenada N del punto 2:").grid(row=2, column=0)
entry_N2 = tk.Entry(ventana)
entry_N2.grid(row=2, column=1)

tk.Label(ventana, text="Coordenada E del punto 2:").grid(row=3, column=0)
entry_E2 = tk.Entry(ventana)
entry_E2.grid(row=3, column=1)

tk.Button(ventana, text="Aceptar", command=aceptar_coordenadas).grid(row=4, columnspan=2)

ventana.mainloop()

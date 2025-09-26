<div align="justify">

# Modelo 3D del Acuífero de Apan mediante Inversión Conjunta de Datos Geofísicos


Este repositorio contiene las herramientas desarrolladas como parte de mi tesis de licenciatura para la visualización, análisis e interpretación de un modelo geofísico del acuífero de Apan, Hidalgo. El modelo fue generado utilizando el algoritmo `gmlayers` a partir de la inversión conjunta tridimensional de datos gravimétricos y magnéticos.

##  Motivación

El acuífero de Apan es una reserva de agua estratégica para la Cuenca del Valle de México. Sin embargo, su geometría tridimensional y sus características internas son poco conocidas. Este proyecto tuvo como objetivo principal generar un modelo detallado para delimitar la extensión de la cuenca y las unidades geológicas que la conforman, así como la estructura subterránea del acuífero, aportando información crucial para la actualización de los modelos existentes del acuifero y una futura gestión sostenible de los recursos hídricos del estado de Hidalgo.

## Funcionamiento del algoritmo

El método se basa en el algoritmo de inversión conjunta propuesto por Gallardo et al. (2003, 2005), el cual minimiza una función objetivo, la cual busca reducir la suma cuadrática de la diferencia entre los datos gravimétricos y magnéticos observados y aquellos calculados para el modelo del subsuelo. El algoritmo prioriza los modelos de variaciones suaves de los relieves de cada capa; lo que se controla a través de parámetros de regularización. Estos parámetros son seleccionados por el usuario, quien a través de experimentación debe buscar que los relieves sean suaves, pero geológicamente razonables.

### Definición del modelo inicial
El modelo del subsuelo se construye a partir de un conjunto de prismas rectangulares que definen una serie de capas geológicas, donde cada capa posee propiedades físicas (densidad y magnetización). La densidad de cada capa no es necesariamente constante, sino que se modela como una función cuadrática de la profundidad (z): 

$\rho(z)=a+bz+cz^{2}$

y un vector de magnetización:

$\mathbf{M} = M_x \hat{\mathbf{i}} + M_y \hat{\mathbf{j}} + M_z \hat{\mathbf{k}}$,


que pueden variar con la profundidad. La inversión busca determinar la profundidad de las interfaces superior $$(h_t)$$ e inferior $$(h_b)$$ entre estas capas.

El modelo inicial se construye utilizando datos geológicos y geofísicos previos, que permiten establecer una primera estimación razonable de estos tres elementos para cada capa. Constituyen el punto de partida y definen la zona de búsqueda para la actualización automática del modelo empleando optimización iterativa que se lleva a cabo considerando los siguientes elementos:

#### a) Función objetivo
En cada iteración, Gmlayers actualiza el modelo empleando un algoritmo de programación cuadrática (Gill et al., 1986), el cual se basa en reducir la función objetivo, que combina el desajuste a los datos observados y la rugosidad del relieve de cada capa. La función objetivo (F) a minimizar se define como:

$$\mathbf{F}(\mathbf{m}) = \min  \| \mathbf{d}_g - \mathbf{g}_z(\mathbf{m}) \|^2_{\mathbf{C}^{-1}_{ddg}} + \| \mathbf{d}_T - \mathbf{T}_t(\mathbf{m}) \|^2_{\mathbf{C}^{-1}_{ddT}} + \| \mathbf{D} \mathbf{m} \|^2_{\mathbf{C}^{-1}_{DD}} + \| \mathbf{m} - \mathbf{m}_R \|^2_{\mathbf{C}^{-1}_{RR}}$$

Donde cada variable representa lo siguiente:

| Símbolo      | Descripción                                                |
|-------------|------------------------------------------------------------|
| $d_g$         | Vector de los datos de gravedad observados                |
| $m$           | Modelo (profundidad a cada prisma para cada capa)         |
| $g_z(m)$      | Respuesta gravimétrica del modelo actual                  |
| $C⁻¹_{ddg}$     | Matriz de covarianza de los datos de gravedad             |
| $d_T$         | Vector de los datos magnéticos observados                |
| $T_t(m)$      | Respuesta magnética del modelo actual                     |
| $C⁻¹_{ddT}$     | Matriz de covarianza de los datos magnéticos             |
| $D$           | Operador de suavidad                                      |
| $m_R$         | Modelo a priori                                           |
| $C⁻¹_{RR}$      | Matriz de covarianza del modelo a priori                 |


#### b) Restricciones de búsqueda
Al emplear técnicas de optimización restringida (programación cuadrática) `gmlayers` permite imponer restricciones a los parámetros para reducir la búsqueda y asegurar la factibilidad del modelo. Estas restricciones se aplican como condiciones de desigualdad:

$$\mathbf{m}_{\text{min}} \leq \mathbf{m} \leq \mathbf{m}_{\text{max}}, \quad \Delta \mathbf{m}_{\text{min}} \leq \Delta \mathbf{m} \leq \Delta \mathbf{m}_{\text{max}}$$

Donde $m_{min}$ y $m_{max}$ representan los límites inferiores y superiores para la profundidad y espesor respectivamente. Para cada prisma en cada capa estas restricciones aseguran que el modelo generado sea consistente y evita la superposición de capas y otras inconsistencias geológicas.

#### c) Búsqueda local y actualización del modelo}

El siguiente paso consiste en realizar una búsqueda lineal alrededor de un modelo de referencia $(\mathbf{m}_0)$. Esto se logra mediante una expansión de Taylor al primer orden de la respuesta gravimétrica $\(\mathbf{g}_z\)$ y magnética $\(\mathbf{T}_t\)$ con respecto a la profundidad $(\mathbf{m})$ de cada prisma.
<p align="center">
$g_z(m) \approx g_z(m_0) + A_g(m_0) (m - m_0)$,
</p>
<p align="center">
$T_t(m) \approx T_t(m_0) + A_T(m_0) (m - m_0)$
</p>

#### d) Evaluación y convergencia
Dada la naturaleza de la función objetivo y las restricciones lineales impuestas, para resolver el problema de minimización planteado en la función objetivo, Gmlayers emplea el algoritmo de programación cuadrática de [48]. 

El proceso iterativo de ajuste continúa hasta que se alcanza la convergencia, es decir, hasta llegar a un punto estacionario o hasta que las diferencias entre los datos observados y los modelados se encuentren dentro de un rango aceptable. Esta convergencia se evalúa mediante los siguientes criterios:


1. Cuando el ajuste entre los datos observados y los modelados es comparable con el nivel de error esperado en los datos. Esto se evalúa mediante el error cuadrático medio normalizado (RMS):
   
<p align="center">
  $RMS = \sqrt{\frac{\sum_{i=1}^n \left( d_i - \hat{d}_i \right)^2}{n}}$,
</p>



donde $\(d_i\)$ son los datos observados, $\(\hat{d}_i\)$ son los datos predichos por el modelo, y $\(n\)$ es el número total de datos.

2. Cuando las profundidades superiores $\(h_t\)$ e inferiores $\(h_b\)$ de los prismas no fluctúan significativamente en iteraciones sucesivas.

3. Cuando la suavidad del modelo es adecuada, evaluada mediante los términos de regularización que penalizan grandes variaciones en las profundidades de los prismas.

El algoritmo `gmlayers` tiene la capacidad de manejar estructuras tridimensionales donde los límites de los prismas que definen el subsuelo no están restringidos a ser planos o simples, sino que deben adaptarse mejor a las estructuras tanto conocidas como esperadas. 


> **Referencias clave:**
> * Gallardo-Delgado, L.A., Pérez-Flores, M.A., & Gómez-Treviño, E. (2003). A versatile algorithm for joint 3D inversion of gravity and magnetic data. *GEOPHYSICS, 68(3)*, 949-959.
> * Gallardo, L.A., Pérez-Flores, M.A., & Gómez-Treviño, E. (2005). Refinement of three-dimensional multilayer models of basins and crustal environments by inversion of gravity and magnetic data. *Tectonophysics, 397(1-2)*, 37-54. 
> * Gill, P. E., Murray, W., Saunders, M. A., & Wright, M. H. (1986). Fortran package for constrained linear least-squares and convex quadratic programming: User’s guide for LSSOL (Version 1.0) (Tech. Rep.). Systems Optimization Laboratory, Stanford University. https://stanford.edu/group/SOL/guides/lssol.pdf.

</div>

## Instalación

Para utilizar estas herramientas, clona el repositorio y asegúrate de tener las dependencias necesarias.

```bash
git clone git@github.com:Livansky/3d-inversion-apan-acuifer.git
cd 3d-inversion-apan-acuifer
pip install -r requirements.txt
```
<div align="justify">
   
## Uso y Ejemplos

### ¿Qué necesitas tener antes de empezar?

#### Datos Gravimétricos: 

Un archivo de texto `gfield.txt` con columnas para las coordenadas UTM (Norte, Este en km), la elevación (Z en km), el valor de la anomalía (g en mgal) y su incertidumbre (sg en mgal).


#### Datos Magnéticos: 

Un archivo de texto `mfield.txt` similar al de gravedad, pero que además incluya al inicio los valores de inclinación y declinación del campo geomagnético, para la fecha y ubicación de los datos.


#### Modelo Geológico Conceptual: 

Una definición clara de las capas geológicas que usarás en el modelo, ordenadas de la más superficial a la más profunda. Para cada capa, necesitas una estimación inicial de sus propiedades (densidad y magnetización)

<div align="center">
  <img src="/images/layers.png" alt="topografiadiscreta" width="300">
</div>


#### Geología Superficial y Topografía: 

Un mapa geológico del área para saber qué unidad geológica aflora en cada punto y un modelo digital de elevación para conocer la topografía.

### Pasos para realizar la inversión usando el algoritmo gmlayers

#### Discretizar el modelo y la geología

El primer paso es crear una rejilla regular sobre tu area de estudio de n filas por m columnas, tú decides el tamaño de los prismas en km y la cantidad. Para hacerlo te puedes apoyar de software como Surfer, solo recuerda, que al final necesitaras saber las coordenadas UTM del centro de cada prisma, guarda un archivo `prismas.txt` con el número de prisma y su coordenada al centro del mismo.

<div align="center">
  <img src="/images/prismas.png" alt="topografiadiscreta" width="400">
</div>


El segundo paso consiste en asignar la topografía promedio del área correspondiente a cada prisma. Puedes hacer una interpolación del tipo nearest neighbor, de manera que al final tengas un archivo `topografia.txt` que contenga las columnas: número de prisma y valor de la elevación.

<div align="center">
  <img src="/images/topografia.png" alt="topografiadiscreta" width="500">
</div>


El siguiente paso consiste en asignar a cada prisma una unidad geológica aflorante según tu mapa geológico y las capas que propusiste a utilizar, recuerda que entre más capas, el modelo podría no distinguirlas unas de otras. Deberás tener un archivo del tipo `capa1.txt` para cada una de las capas de tu modelo, de manera que contenga únicamente una columna con los prismas asignados a esa unidad.

#### Generar los archivos de restricciones de capas

ejecuta `program1.exe` este solicitará una serie de parámetros geométricos de la base de la capa; el número de la capa; el número de prismas, los valores $x_{\text{min}}$, $x_0$ y $x_{\text{max}}$ de la base de la capa i.e., el caso donde aflora cualquier unidad por debajo de la capa que se está trabajando), los cuales pueden ser constantes o variables. Si el valor se toma de la topografía, se digita 10,000;  la desviación estándar ($sx0$); los espesores mínimo y máximo ($Esp_{{min}}$, $Esp_{{max}}$) de la base; y por último, se solicita el archivo que contenga la información topográfica-batimétrica \emph{i.e.}, el número de prisma y su elevación correspondiente `topografia.txt`. Este programa se ejecuta una vez por capa

Posteriormente, ejecuta `program2.exe`, el objetivo de este segundo programa es asegurar que los prismas que están aflorando, i.e., los que corresponden a la geología superficial observada en los mapas geológicos tengan las restricciones necesarias y el modelo refleje correctamente las condiciones observadas. Dado que se trabaja con múltiples capas, existen varios casos a considerar además del caso base (i.e., cuando aflora cualquier unidad por debajo de la capa a trabajar). El siguiente caso a considerar es cuando aflora la unidad que se está trabajando; para ello, se vuelve a ejecutar el programa, pero ahora utilizando como archivo de entrada el archivo que resultó de la primera iteración (donde se empleó el archivo generado por el primer programa). Posteriormente, por cada unidad que aflora por encima de la capa en cuestión, se repite el proceso utilizando el archivo de entrada generado en la ejecución anterior. Finalmente, el archivo resultante para cada capa se pega por debajo del archivo anterior y una vez todos juntos se pega por debajo del archivo `Model.txt`

Para más detalles sobre este procedimiento puede consultar https://tesiunamdocumentos.dgb.unam.mx/ptd2025/abr_jun/0870941/Index.html
















## Resultados de la Tesis

A continuación se muestran algunos de los resultados generados con estas herramientas, que fueron clave para la interpretación geológica final.

**Mapa de Espesor de la Capa de Sedimentos**
![Mapa de espesor de sedimentos](imagenes/resultado_mapa_espesor.png)
*Este mapa revela las zonas de mayor acumulación de sedimentos, coincidiendo con las depresiones tectónicas principales de la cuenca.*

**Sección Geológica A-A'**
![Corte geológico A-A'](imagenes/resultado_corte_A-A.png)
*Esta sección muestra claramente la estructura de graben de la cuenca, delimitada por la falla Apan-Tlaloc.*

## Mis Herramientas de Visualización

El algoritmo `gmlayers` produce archivos de texto con las profundidades de las interfaces para cada prisma del modelo. Para interpretar estos resultados, desarrollé dos herramientas en Python:

1.  **`visualizador_cortes.py`**: Este script toma el archivo de salida del modelo y genera secciones transversales (cortes geológicos) en cualquier dirección (N-S o E-W), permitiendo visualizar la estructura interna de la cuenca.
2.  **`generador_mapas_espesor.py`**: Esta herramienta calcula y grafica los mapas de espesores para cada una de las capas geológicas definidas en el modelo, ayudando a identificar las zonas de mayor acumulación de materiales.



## Contacto

[Tu Nombre] - [Tu Email] - [Link a tu LinkedIn]

</div>

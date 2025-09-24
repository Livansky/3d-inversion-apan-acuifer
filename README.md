# Modelo 3D del Acuífero de Apan mediante Inversión Conjunta de Datos Geofísicos

![Banner con un mapa de la tesis] /images/unnamed.png

Este repositorio contiene las herramientas desarrolladas como parte de mi tesis de licenciatura para la visualización, análisis e interpretación de un modelo geofísico del acuífero de Apan, Hidalgo. El modelo fue generado utilizando el algoritmo `gmlayers` a partir de la inversión conjunta tridimensional de datos gravimétricos y magnéticos.

##  Motivación

El acuífero de Apan es una reserva de agua estratégica para la Cuenca del Valle de México. Sin embargo, su geometría tridimensional y sus características internas son poco conocidas. Este proyecto tuvo como objetivo principal generar un modelo detallado para delimitar la extensión de la cuenca y las unidades geológicas que la conforman, así como la estructura subterranea del acuífero, aportando información crucial para la actualización de los modelos existentes del acuifero y una futura gestión sostenible de los recursos hídricos del estado de Hidalgo.

## Funcionamiento del algoritmo

El método se basa en el algoritmo de inversión conjunta propuesto por Gallardo et al. (2003, 2005), el cual minimiza una función objetivo, la cual busca reducir la suma cuadrática de la diferencia entre los datos gravimétricos y magnéticos observados y aquellos calculados para el modelo del subsuelo. El algoritmo privilegia los modelos de variaciones suaves de los relieves de cada capa; lo que se controla a través de parámetros de regularización. Estos parámetros son seleccionados por el usuario, quien a través de experimentación debe buscar que los relieves sean suaves, pero geológicamente razonables.

### Definición del modelo inicial
El modelo del subsuelo se construye a partir de un conjunto de prismas rectangulares que definen una serie de capas geológicas, donde cada capa posee propiedades físicas (densidad y magnetización) 

La densidad de cada capa no es necesariamente constante, sino que se modela como una función cuadrática de la profundidad (z): 
<p align="center">
$\rho(z)=a+bz+cz^{2}$
</p>
y un vector de magnetización:
<p align="center">
$\mathbf{M} = M_x \hat{\mathbf{i}} + M_y \hat{\mathbf{j}} + M_z \hat{\mathbf{k}}$,
</p>

que pueden variar con la profundidad. La inversión busca determinar la profundidad de las interfaces superior $$(h_t)$$ e inferior $$(h_b)$$ entre estas capas.

El modelo inicial se construye utilizando datos geológicos y geofísicos previos, que permiten establecer una primera estimación razonable de estos tres elementos para cada capa. Constituyen el punto de partida y definen la zona de búsqueda para la actualización automática del modelo empleando optimización iterativa que se lleva a cabo considerando los siguientes elementos:

#### a) Función objetivo
En cada iteración, Gmlayers actualiza el modelo empleando un algoritmo de programación cuadrática el cual se basa en reducir la función objetivo, que combina el desajuste a los datos observados y la rugosidad del relieve de cada capa. La función objetivo (F) a minimizar se define como:

$$\mathbf{F}(\mathbf{m}) = \min  \| \mathbf{d}_g - \mathbf{g}_z(\mathbf{m}) \|^2_{\mathbf{C}^{-1}_{ddg}} + \| \mathbf{d}_T - \mathbf{T}_t(\mathbf{m}) \|^2_{\mathbf{C}^{-1}_{ddT}} + \| \mathbf{D} \mathbf{m} \|^2_{\mathbf{C}^{-1}_{DD}} + \| \mathbf{m} - \mathbf{m}_R \|^2_{\mathbf{C}^{-1}_{RR}}$$

#### b) Restricciones de búsqueda
Al emplear técnicas de optimización restringida (programación cuadrática) Gmlayers permite imponer restricciones a los parámetros para reducir la búsqueda y asegurar la factibilidad del modelo. Estas restricciones se aplican como condiciones de desigualdad:

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

El algoritmo Gmlayers tiene la capacidad de manejar estructuras tridimensionales donde los límites de los prismas que definen el subsuelo no están restringidos a ser planos o simples, sino que deben adaptarse mejor a las estructuras tanto conocidas como esperadas 


> **Referencias clave:**
> * Gallardo-Delgado, L.A., Pérez-Flores, M.A., & Gómez-Treviño, E. (2003). A versatile algorithm for joint 3D inversion of gravity and magnetic data. *GEOPHYSICS, 68(3)*, 949-959.
> * Gallardo, L.A., Pérez-Flores, M.A., & Gómez-Treviño, E. (2005). Refinement of three-dimensional multilayer models of basins and crustal environments by inversion of gravity and magnetic data. *Tectonophysics, 397(1-2)*, 37-54. 
> * 

## Mis Herramientas de Visualización

El algoritmo `gmlayers` produce archivos de texto con las profundidades de las interfaces para cada prisma del modelo. Para interpretar estos resultados, desarrollé dos herramientas en Python:

1.  **`visualizador_cortes.py`**: Este script toma el archivo de salida del modelo y genera secciones transversales (cortes geológicos) en cualquier dirección (N-S o E-W), permitiendo visualizar la estructura interna de la cuenca.
2.  **`generador_mapas_espesor.py`**: Esta herramienta calcula y grafica los mapas de espesores para cada una de las capas geológicas definidas en el modelo, ayudando a identificar las zonas de mayor acumulación de materiales.

## Instalación

Para utilizar estas herramientas, clona el repositorio y asegúrate de tener las dependencias necesarias.

```bash
git clone [https://github.com/tu-usuario/modelo-acuifero-apan.git](https://github.com/tu-usuario/modelo-acuifero-apan.git)
cd modelo-acuifero-apan
pip install -r requirements.txt
```

## Uso y Ejemplos

La forma más sencilla de ver cómo funcionan las herramientas es a través del Jupyter Notebook incluido en la carpeta `/notebooks`.

**`notebooks/2_Visualizacion_del_Modelo.ipynb`**

En este notebook se muestra un ejemplo completo:
* Carga de un archivo de salida de `gmlayers` de muestra (de `datos/gmlayers_output_muestra.txt`).
* Uso de la herramienta `visualizador_cortes` para generar un perfil.
* Uso de la herramienta `generador_mapas_espesor` para crear el mapa de la capa de sedimentos.

## Resultados de la Tesis

A continuación se muestran algunos de los resultados generados con estas herramientas, que fueron clave para la interpretación geológica final.

**Mapa de Espesor de la Capa de Sedimentos**
![Mapa de espesor de sedimentos](imagenes/resultado_mapa_espesor.png)
*Este mapa revela las zonas de mayor acumulación de sedimentos, coincidiendo con las depresiones tectónicas principales de la cuenca.*

**Sección Geológica A-A'**
![Corte geológico A-A'](imagenes/resultado_corte_A-A.png)
*Esta sección muestra claramente la estructura de graben de la cuenca, delimitada por la falla Apan-Tlaloc.*

## Contacto

[Tu Nombre] - [Tu Email] - [Link a tu LinkedIn]

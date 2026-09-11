# Guía 1: Geometría en el Plano, Linux y Python

**Curso:** Robótica del Servicio (`ING 01335`)  
**Facultad:** Facultad de Ingeniería  
**Institución:** Politécnico Colombiano Jaime Isaza Cadavid  
**Docente:** Deimer Miranda Montoya, MSc.(c). (`deimer_miranda91162@elpoli.edu.co`)  
**Periodo Académico:** 2026-2  

---

| **Tiempo Estimado** | **Modalidad** | **Entregables** |
| :---: | :---: | :---: |
| 3 horas de trabajo independiente | Desarrollo individual | Desarrollo matemático, código Python y gráficas de validación |

---

## 1. Propósito de la guía

Esta guía tiene como propósito fortalecer los fundamentos matemáticos necesarios para representar la posición y dirección de movimiento de un robot móvil en un plano bidimensional.

Al finalizar las actividades, el estudiante deberá estar en capacidad de:

* Representar puntos y vectores en el plano cartesiano;
* Calcular vectores de desplazamiento;
* Calcular la magnitud de un vector;
* Determinar distancias entre posiciones;
* Convertir ángulos entre grados y radianes;
* Calcular la dirección de un vector;
* Aplicar correctamente la función $\operatorname{atan2}$;
* Identificar el cuadrante asociado a un desplazamiento;
* Interpretar sistemas de referencia globales y locales;
* Utilizar Linux para organizar archivos de trabajo;
* Utilizar Python para verificar cálculos matemáticos;
* Representar gráficamente posiciones, vectores y metas.

> [!NOTE]
> **Regla fundamental:**  
> **Primero calcular manualmente y después validar computacionalmente.**  
> Python no reemplaza el razonamiento matemático; se utiliza como herramienta para comprobar, visualizar y analizar los resultados.

---

## 2. Fundamentos matemáticos

### 2.1. Representación de un punto

Una posición en un plano bidimensional puede representarse mediante el vector columna:

$$P = \begin{bmatrix} x \\ y \end{bmatrix}$$

donde $x$ representa la coordenada horizontal y $y$ la coordenada vertical.

> [!NOTE]
> **Punto:** Un punto representa una ubicación dentro de un sistema de referencia. En robótica móvil puede representar la posición del robot, una meta, un obstáculo o cualquier elemento relevante del entorno.

---

### 2.2. Vector entre dos puntos

Sean dos puntos:

$$P_1 = \begin{bmatrix} x_1 \\ y_1 \end{bmatrix}, \qquad P_2 = \begin{bmatrix} x_2 \\ y_2 \end{bmatrix}$$

el vector que permite desplazarse desde $P_1$ hasta $P_2$ se obtiene mediante la resta vectorial:

$$\mathbf{d} = P_2 - P_1 = \begin{bmatrix} x_2 - x_1 \\ y_2 - y_1 \end{bmatrix} = \begin{bmatrix} \Delta x \\ \Delta y \end{bmatrix}$$

donde:
$$\Delta x = x_2 - x_1$$
$$\Delta y = y_2 - y_1$$

---

### 2.3. Magnitud de un vector y Distancia Euclidiana

La longitud o magnitud de un vector se calcula mediante su norma euclidiana:

$$\|\mathbf{d}\| = \sqrt{(\Delta x)^2 + (\Delta y)^2}$$

En el caso de dos posiciones, esta expresión corresponde a la distancia euclidiana:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

---

### 2.4. Ejemplo resuelto paso a paso

Suponga que un robot está ubicado en la posición inicial $P_R = (-2, 1)$ y desea dirigirse hacia la meta $P_G = (3, 5)$.

1. **Desplazamiento horizontal:**
   $$\Delta x = 3 - (-2) = 5$$

2. **Desplazamiento vertical:**
   $$\Delta y = 5 - 1 = 4$$

3. **Vector de desplazamiento:**
   $$\mathbf{d} = \begin{bmatrix} 5 \\ 4 \end{bmatrix}$$

4. **Distancia:**
   $$d = \sqrt{5^2 + 4^2} = \sqrt{25 + 16} = \sqrt{41} \approx 6.40$$

> [!TIP]
> El vector $(5, 4)$ indica la dirección y sentido geométrico de avance, mientras que la magnitud $\|\mathbf{d}\| \approx 6.40$ unidades indica la distancia a recorrer.

---

## 3. Ángulos y orientación

### 3.1. Grados y radianes

La relación angular fundamental es:

$$180^\circ = \pi\text{ rad}$$

Factores de conversión:
$$\theta_{\mathrm{rad}} = \theta_{\mathrm{deg}} \cdot \frac{\pi}{180}$$
$$\theta_{\mathrm{deg}} = \theta_{\mathrm{rad}} \cdot \frac{180}{\pi}$$

---

### 3.2. Dirección de un vector

Para un vector de desplazamiento $\mathbf{d} = \begin{bmatrix} \Delta x \\ \Delta y \end{bmatrix}$, su orientación respecto al semieje positivo $X$ se calcula como:

$$\theta = \operatorname{atan2}(\Delta y, \Delta x)$$

---

### 3.3. Cálculo manual de atan2 y corrección por cuadrantes

Si se utiliza la tangente inversa convencional $\theta_0 = \tan^{-1}\left(\frac{\Delta y}{\Delta x}\right)$, se debe aplicar la corrección de cuadrante:

| Condición $\Delta x$ | Condición $\Delta y$ | Cuadrante / Caso | Corrección Angular $\theta$ |
| :---: | :---: | :---: | :---: |
| $\Delta x > 0$ | Cualquier valor | Cuadrante I o IV | $\theta = \theta_0$ |
| $\Delta x < 0$ | $\Delta y \ge 0$ | Cuadrante II | $\theta = \theta_0 + 180^\circ$ |
| $\Delta x < 0$ | $\Delta y < 0$ | Cuadrante III | $\theta = \theta_0 - 180^\circ$ (o $\theta_0 + 180^\circ$) |
| $\Delta x = 0$ | $\Delta y > 0$ | Eje $+Y$ | $\theta = +90^\circ\ (+ \pi/2\text{ rad})$ |
| $\Delta x = 0$ | $\Delta y < 0$ | Eje $-Y$ | $\theta = -90^\circ\ (- \pi/2\text{ rad})$ |
| $\Delta x = 0$ | $\Delta y = 0$ | Origen | Indefinido |

> [!WARNING]
> No utilice únicamente $\tan^{-1}(\Delta y / \Delta x)$ sin verificar el signo de $\Delta x$ y $\Delta y$. Dos vectores opuestos (ej. $(1, 1)$ y $(-1, -1)$) producen el mismo cociente $+1$, pero apuntan a $+45^\circ$ y $-135^\circ$ respectivamente.

---

## 4. Ejercicios de desarrollo manual

### 4.1. Nivel 1: Puntos y vectores
Para cada pareja calcule $\Delta x$, $\Delta y$, $\mathbf{d} = P_2 - P_1$:

1. $P_1 = (1, 3), \quad P_2 = (7, 8)$
2. $P_1 = (-2, 4), \quad P_2 = (5, 1)$
3. $P_1 = (6, -3), \quad P_2 = (2, 5)$
4. $P_1 = (-4, -2), \quad P_2 = (3, 6)$
5. $P_1 = (5, 7), \quad P_2 = (-1, 2)$
6. $P_1 = (-6, 3), \quad P_2 = (-2, -5)$

---

### 4.2. Nivel 2: Magnitud y distancia
Calcule el vector $\mathbf{d}$ y su norma euclidiana $d = \|\mathbf{d}\|$:

7. $P_1 = (0, 0), \quad P_2 = (8, 6)$
8. $P_1 = (-3, 2), \quad P_2 = (1, 5)$
9. $P_1 = (4, -1), \quad P_2 = (-2, 7)$
10. $P_1 = (-5, -4), \quad P_2 = (1, -1)$
11. $P_1 = (3, 8), \quad P_2 = (9, 0)$
12. $P_1 = (-7, 1), \quad P_2 = (-2, 13)$

---

### 4.3. Nivel 3: Conversión Grados y Radianes

**Convertir a radianes:**
13. $30^\circ$
14. $45^\circ$
15. $120^\circ$
16. $225^\circ$
17. $-60^\circ$
18. $315^\circ$

**Convertir a grados:**
19. $\frac{\pi}{6}\text{ rad}$
20. $\frac{2\pi}{3}\text{ rad}$
21. $-\frac{\pi}{4}\text{ rad}$
22. $\frac{5\pi}{3}\text{ rad}$

---

### 4.4. Nivel 4: Dirección y cuadrantes
Para cada vector determine cuadrante, $\theta_0$, corrección en grados y radianes:

23. $\mathbf{v}_1 = \begin{bmatrix} 5 \\ 2 \end{bmatrix}$
24. $\mathbf{v}_2 = \begin{bmatrix} -4 \\ 7 \end{bmatrix}$
25. $\mathbf{v}_3 = \begin{bmatrix} -6 \\ -3 \end{bmatrix}$
26. $\mathbf{v}_4 = \begin{bmatrix} 2 \\ -8 \end{bmatrix}$
27. $\mathbf{v}_5 = \begin{bmatrix} 0 \\ 5 \end{bmatrix}$
28. $\mathbf{v}_6 = \begin{bmatrix} -7 \\ 0 \end{bmatrix}$

---

### 4.5. Nivel 5: Posición del Robot y Meta
Calcule $\Delta x, \Delta y, d, \theta_g = \operatorname{atan2}(\Delta y, \Delta x)$ y cuadrante relativo:

29. $P_R = (2, -1), \quad P_G = (8, 3)$
30. $P_R = (5, 2), \quad P_G = (-1, 7)$
31. $P_R = (-2, 6), \quad P_G = (-8, 1)$
32. $P_R = (-4, -3), \quad P_G = (3, -7)$
33. $P_R = (6, -2), \quad P_G = (6, 7)$
34. $P_R = (3, 5), \quad P_G = (-5, 5)$

---

### 4.6. Nivel 6: Preguntas de Interpretación
35. Si $\Delta x > 0$ y $\Delta y > 0$, ¿en qué cuadrante se encuentra la meta respecto al robot?
36. Si $\Delta x < 0$ y $\Delta y > 0$, ¿qué corrección debe hacerse sobre el resultado de la tangente inversa?
37. ¿Puede existir un vector con magnitud igual a cero y dirección definida? Explique.
38. ¿Qué significa físicamente que $d = 0$?
39. ¿Qué ocurre con $\operatorname{atan2}(\Delta y, \Delta x)$ cuando $\Delta x = 0$ y $\Delta y > 0$?
40. ¿Por qué conocer únicamente la distancia no es suficiente para realizar navegación autónoma?

---

## 5. Práctica en Linux y Organización

Comandos básicos de terminal:

```bash
pwd
mkdir -p ~/robotica_servicio/guia_01
cd ~/robotica_servicio/guia_01
touch geometria_robot.py
gedit geometria_robot.py # o nano / code
```

---

## 6. Validación Matemática y Visualización con Python

> [!NOTE]
> **Ubicación sugerida en el repositorio:**  
> Estos scripts de análisis geométrico y cinemático preliminar se integran en los módulos de pruebas del repositorio o en scripts de experimentación offline dentro de [`stage_01_motor_instrumentation/`](../../stage_01_motor_instrumentation/).

### 6.1. Script de Cálculo Matemático (`geometria_robot.py`)

```python
import math

xr, yr = -3, 1
xg, yg = 4, -4

dx = xg - xr
dy = yg - yr

distancia = math.sqrt(dx**2 + dy**2)
angulo_rad = math.atan2(dy, dx)
angulo_deg = math.degrees(angulo_rad)

print(f"Delta x: {dx}")
print(f"Delta y: {dy}")
print(f"Distancia: {distancia:.4f}")
print(f"Angulo [rad]: {angulo_rad:.4f}")
print(f"Angulo [deg]: {angulo_deg:.2f}°")
```

---

### 6.2. Script de Visualización con Matplotlib

```python
import matplotlib.pyplot as plt

xr, yr = -3, 1
xg, yg = 4, -4

dx = xg - xr
dy = yg - yr

plt.figure(figsize=(7, 7))
plt.scatter(xr, yr, color="blue", s=100, label="Robot $P_R$")
plt.scatter(xg, yg, color="red", s=100, label="Meta $P_G$")

plt.quiver(
    xr, yr, dx, dy,
    angles="xy",
    scale_units="xy",
    scale=1,
    color="darkgreen",
    label="Vector Desplazamiento $\mathbf{d}$"
)

plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)

plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title(f"Trayectoria: Distancia={math.sqrt(dx**2+dy**2):.2f}, Ángulo={math.degrees(math.atan2(dy,dx)):.1f}°")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()
```

---

## 7. Reto Integrador: Navegación Multiobjetivo

Considere la siguiente secuencia consecutiva de puntos de navegación:

$$P_R = (0, 0) \rightarrow P_1 = (4, 3) \rightarrow P_2 = (-2, 7) \rightarrow P_3 = (-6, -1) \rightarrow P_4 = (3, -5)$$

1. Calcule manualmente $\Delta x, \Delta y, \mathbf{d}, d, \theta_{\mathrm{deg}}, \theta_{\mathrm{rad}}$ para cada tramo.
2. Implemente un script en Python que itere sobre la lista de puntos, calcule la distancia acumulada total y grafique la trayectoria con flechas direccionales.

---

## 8. Relación con la Instrumentación del Motor DC (Stage 01)

En el sistema de control de motor DC de este repositorio ([`stage_01_motor_instrumentation`](../../stage_01_motor_instrumentation)):
* La posición angular $\theta(t)$ del rotor se obtiene a partir de la cuenta discreta de pulsos del encoder de cuadratura:
  $$\theta(t) = \frac{2\pi \cdot \Delta \text{ticks}}{N_{\mathrm{rev}}} \quad [\text{rad}], \qquad N_{\mathrm{rev}} = 960\ \text{ticks/rev}$$
* La velocidad angular $\omega(t)$ se calcula por derivación numérica en tiempo discreto ($T_s = 0.1\text{ s}$):
  $$\omega(t) = \frac{\theta(k) - \theta(k-1)}{T_s} = \frac{2\pi \cdot \Delta \text{count}}{N_{\mathrm{rev}} \cdot T_s} \quad [\text{rad/s}]$$
  código implementado en el firmware del ESP32: [`firmware/esp32_motor_step/src/main.cpp`](../../firmware/esp32_motor_step/src/main.cpp#L140-L157).

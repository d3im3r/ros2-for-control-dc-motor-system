# Guía 2: Identificación Experimental Mediante Prueba Escalón

<div align="center">

**Asignatura:** Control Inteligente (`ING01343-ING278`)  
**Institución:** Politécnico Colombiano Jaime Isaza Cadavid — Facultad de Ingeniería  
**Docente:** Deimer Miranda Montoya, MSc.(c) — `deimer_miranda91162@elpoli.edu.co`  
**Período Académico:** 2026-2  
**Modalidad:** Trabajo práctico guiado (Individual o parejas)  
**Entregables:** Curvas de reacción experimentales, archivos CSV registrados y modelos matemáticos FOP y FOPDT identificados

</div>

---

## 1. Introducción

En la **Guía 1** se construyó y validó el nodo micro-ROS `motor_step_node`, capaz de recibir una referencia de PWM, accionar el motor DC, estimar su velocidad angular mediante un encoder incremental y publicar dicha medición hacia ROS 2. La calibración experimental realizada sobre el montaje estableció:

$$\boxed{N_{\mathrm{rev}} = 960\ \text{ticks/rev}}$$

En esta segunda guía se utilizará el sistema instrumentado para realizar **identificación paramétrica experimental en lazo abierto**. El procedimiento se basará en la respuesta del motor ante entradas escalón de PWM y en el análisis de su curva de reacción temporal. A partir de los datos entrada-salida se propondrán y compararán dos modelos de aproximación dinámica:

1. **Modelo de Primer Orden Puro (FOP — *First Order Plus*):**
   $$G_{\mathrm{FOP}}(s) = \frac{K}{\tau s + 1}$$

2. **Modelo de Primer Orden con Tiempo Muerto (FOPDT — *First Order Plus Dead Time*):**
   $$G_{\mathrm{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$$

> [!TIP]
> **Enfoque Metodológico:**
> La identificación experimental busca obtener un modelo matemático simplificado y representativo que capture la dinámica dominante del sistema dentro del rango operativo real, permitiendo diseñar posteriormente controladores eficaces.

---

### 1.1. Resultados de Aprendizaje

Al finalizar la guía, el estudiante estará en capacidad de:

1. Realizar pruebas escalón repetibles y automatizadas sobre el motor DC.
2. Registrar simultáneamente la señal de entrada PWM y la velocidad angular en archivos CSV estructurados.
3. Interpretar la curva de reacción experimental del sistema físico.
4. Extraer el valor inicial $\omega_0$ y el régimen permanente $\omega_{ss}$.
5. Calcular la ganancia estática $K$ del sistema.
6. Estimar la constante de tiempo $\tau$ mediante el criterio del $63.2\,\%$ de la respuesta total.
7. Estimar el retardo aparente $\theta$ cuando sea observable en el transitorio.
8. Construir modelos de transferencia FOP y FOPDT a partir de datos reales.
9. Comparar los parámetros obtenidos en diferentes puntos de operación ($30\,\%$, $45\,\%$ y $60\,\%$ PWM).
10. Evaluar si un único modelo lineal representa adecuadamente la planta o si existen efectos no lineales relevantes.

---

## 2. Punto de Partida: Sistema Instrumentado

Se parte del sistema de instrumentación validado con la siguiente arquitectura de comunicación:

| Tópico | Dirección | Tipo de Mensaje | Descripción |
| :--- | :---: | :---: | :--- |
| `/pwm_input` | PC $\rightarrow$ ESP32 | `std_msgs/msg/Float32` | Referencia PWM en porcentaje $[-100.0, 100.0]\,\%$ |
| `/vel_rad_s` | ESP32 $\rightarrow$ PC | `std_msgs/msg/Float32` | Velocidad angular en $\text{rad/s}$ ($T_s = 0.1\text{ s}$) |
| `/vel_rpm` | ESP32 $\rightarrow$ PC | `std_msgs/msg/Float32` | Velocidad angular en $\text{rpm}$ |

$$\omega[k] = \frac{2\pi \Delta N[k]}{960 \Delta t}\quad [\text{rad/s}]$$

> [!CAUTION]
> Antes de iniciar las pruebas de identificación, verifique que la medición de velocidad angular responda sin retardos espurios y que el motor se detenga completamente al enviar `0.0` a `/pwm_input`.

---

## 3. Fundamento: Identificación Experimental de la Planta

La identificación experimental modela la relación entrada-salida considerando:

* **Entrada:** $u(t) = \text{PWM aplicado } [\%]$
* **Salida:** $\omega(t) = \text{Velocidad angular } [\text{rad/s}]$

$$\boxed{G_{\mathrm{exp}}(s) = \frac{\Omega(s)}{U_{\mathrm{PWM}}(s)}}$$

```mermaid
flowchart LR
    STEP["Prueba Escalón<br>(Launch automatizado)"] --> DATA["Adquisición<br>(u(t), ω(t))"]
    DATA --> CURVE["Curva de Reacción<br>(Gráfica temporal)"]
    CURVE --> STRUCT["Estructura<br>(FOP / FOPDT)"]
    STRUCT --> PARAM["Ajuste de Parámetros<br>(K, τ, θ)"]
    PARAM --> MODEL["Modelo Matemático<br>G(s)"]
```

> [!NOTE]
> **Curva de Reacción:**
> Es la respuesta temporal medida de la velocidad angular del motor frente a un cambio tipo escalón en la entrada PWM. Su perfil permite estimar las constantes dinámicas y la ganancia del proceso.

---

## 4. Estructuras de Modelado: FOP vs. FOPDT

Aunque el motor DC posee una dinámica electromecánica de segundo orden (dinámica eléctrica por inductancia de armadura + dinámica mecánica por inercia y fricción), la constante de tiempo eléctrica $\tau_e = L_a/R_a$ es órdenes de magnitud más rápida que la constante mecánica $\tau_m = J/b$. Por tanto, el comportamiento observable de velocidad se modela con alta fidelidad como un sistema de primer orden:

* **Modelo FOP (Primer Orden Puro):**
  $$\boxed{G_{\mathrm{FOP}}(s) = \frac{K}{\tau s + 1}}$$
  * $K$: Ganancia estática en $\left[\frac{\text{rad/s}}{\%\,\text{PWM}}\right]$.
  * $\tau$: Constante de tiempo en $[\text{s}]$.

* **Modelo FOPDT (Primer Orden con Retardo Aparente):**
  $$\boxed{G_{\mathrm{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}}$$
  * $\theta$: Retardo o tiempo muerto aparente en $[\text{s}]$.

---

## 5. Arquitectura ROS 2 para la Prueba Escalón

```mermaid
flowchart TD
    PWM["/pwm_input<br>(Float32, %)"] --> MOTOR(["motor_step_node<br>(ESP32 / micro-ROS)"])
    MOTOR --> RAD["/vel_rad_s<br>(Float32, rad/s)"]
    MOTOR --> RPM["/vel_rpm<br>(Float32, rpm)"]

    PWM -.-> DB(["step_response_DB<br>(data_logger.py)"])
    RAD --> DB
    RAD --> GRAPH(["vel_ang_motor<br>(velocity_monitor.py)"])
```

---

## 6. Scripts de Adquisición y Visualización en ROS 2

Los nodos ejecutables están disponibles en el paquete `dc_motor_experiments`:

### 6.1. Registrador de Datos a CSV (`data_logger.py`)
* Ubicación: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py`](../../ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py)
* Genera archivos con nombre: `motor_step_response_YYYYMMDD_HHMMSS.csv`

```csv
Time (s),Angular Velocity (rad/s),PWM (%)
0.100,0.000000,0.000
0.200,0.000000,0.000
...
1.100,2.152431,45.000
...
36.100,45.892100,0.000
```

### 6.2. Visualizador en Tiempo Real (`velocity_monitor.py`)
* Ubicación: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/velocity_monitor.py`](../../ros2_ws/src/dc_motor_experiments/dc_motor_experiments/velocity_monitor.py)
* Grafica dinámicamente $\omega(t)$ vs $t$ con Matplotlib a $10\text{ Hz}$.

---

## 7. Diseño de las Pruebas Experimentales

Se realizarán tres ensayos independientes para caracterizar la planta a diferentes niveles de excitación:

| Ensayo | $u_0$ ($\%$) | $u_{\text{step}}$ ($\%$) | Duración Total | Muestras ($10\text{ Hz}$) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | $0\,\%$ | $30\,\%$ | $40.0\text{ s}$ | $400$ muestras |
| **2** | $0\,\%$ | $45\,\%$ | $40.0\text{ s}$ | $400$ muestras |
| **3** | $0\,\%$ | $60\,\%$ | $40.0\text{ s}$ | $400$ muestras |

---

## 8. Automatización de la Prueba Mediante Launch File

Para garantizar que todas las pruebas tengan exactamente la misma secuencia temporal y sean comparables, se utiliza el launch file:

* Ubicación del Launch en el repositorio: [`ros2_ws/src/dc_motor_bringup/launch/stage_02_identification.launch.py`](../../ros2_ws/src/dc_motor_bringup/launch/stage_02_identification.launch.py)

### Perfil Temporal del Ensayo:

```text
  PWM (%)
     ^
     |              +-----------------------------------+
step |              |                                   |
     |              |         Escalón (35.0 s)          |
     |              |                                   |
  0% +--------------+                                   +---------------> Tiempo (s)
     0             1.0                                 36.0           40.0
        (Reposo 1s)                                      (Reposo fin 4s)
```

1. **Reposo Inicial ($0.0\text{ s} - 1.0\text{ s}$):** Entrada en $0\,\%$ para registrar la condición inicial $\omega_0$.
2. **Escalón Activo ($1.0\text{ s} - 36.0\text{ s}$):** Aplicación de $u_{\text{step}}\,\%$ durante $35.0\text{ s}$ para alcanzar régimen permanente.
3. **Reposo Final ($36.0\text{ s} - 40.0\text{ s}$):** Regreso a $0\,\%$ para frenado seguro.

### Ejecución de los Ensayos:

```bash
# Compilar y cargar el workspace
cd ~/ros2-for-control-dc-motor-system/ros2_ws
colcon build --symlink-install
source install/setup.bash

# Ensayo 1: Escalón al 30%
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=30.0

# Ensayo 2: Escalón al 45%
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0

# Ensayo 3: Escalón al 60%
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=60.0
```

---

## 9. Construcción y Análisis de la Curva de Reacción

Del archivo CSV se extraen los siguientes puntos característicos:

* $t_0$: Instante exacto de aplicación del escalón ($1.0\text{ s}$).
* $u_0, u_{ss}$: Amplitud del PWM antes y durante el escalón.
* $\omega_0$: Velocidad media antes de $t_0$ ($\approx 0\text{ rad/s}$).
* $\omega_{ss}$: Velocidad media en régimen permanente estacionario.

---

## 10. Estimación de la Ganancia Estática ($K$)

$$\boxed{K = \frac{\Delta\omega}{\Delta u} = \frac{\omega_{ss} - \omega_0}{u_{ss} - u_0}\quad \left[\frac{\text{rad/s}}{\%\,\text{PWM}}\right]}$$

Partiendo desde reposo ($u_0 = 0$, $\omega_0 \approx 0$):

$$K \approx \frac{\omega_{ss}}{u_{ss}}$$

---

## 11. Modelo FOP: Estimación de la Constante de Tiempo ($\tau$)

La respuesta analítica de un sistema FOP ante entrada escalón es:

$$\omega(t) = \omega_0 + \Delta\omega \left(1 - e^{-(t - t_0)/\tau}\right), \qquad t \geq t_0$$

Para $t - t_0 = \tau$:

$$1 - e^{-1} = 1 - 0.367879 = 0.63212 \approx 63.2\,\%$$

$$\boxed{\omega_{63.2} = \omega_0 + 0.632\,(\omega_{ss} - \omega_0)}$$

Se busca en los datos el instante $t_{63.2}$ donde $\omega(t_{63.2}) \approx \omega_{63.2}$:

$$\boxed{\tau_{\mathrm{FOP}} = t_{63.2} - t_0}$$

```text
  ω(t) ^
       |                                              ...  ω_ss
       |                                  . ''''''''''
       |                          . '
ω_63.2 |-------------+---------.'
       |             |       . '
       |             |   . '
   ω_0 +-------------+.'
       0            t_0       t_63.2                         ---> Tiempo (s)
                     |<-- τ -->|
```

---

## 12. Modelo FOPDT: Incorporación del Retardo ($\theta$)

Si existe un retardo aparente $\theta$ entre $t_0$ y el instante $t_{\text{inicio}}$ en el que la velocidad comienza a elevarse:

$$\boxed{\theta \approx t_{\text{inicio}} - t_0}$$

$$t_{63.2} = t_0 + \theta + \tau$$

$$\boxed{\tau_{\mathrm{FOPDT}} = t_{63.2} - t_0 - \theta}$$

```text
  ω(t) ^
       |                                              ...  ω_ss
       |                                  . ''''''''''
       |                          . '
ω_63.2 |-----------------------.'
       |                     . '
       |                 . '
   ω_0 +-------------+---+.'
       0            t_0 t_ini t_63.2                         ---> Tiempo (s)
                     | θ |<-- τ -->|
```

---

## 13. Comparación y Ajuste Offline con Scripts de Python

Los scripts automatizados de identificación se encuentran en:

* **Identificación FOP:** [`stage_02_system_identification/analysis/identify_fop.py`](../../stage_02_system_identification/analysis/identify_fop.py)
* **Identificación FOPDT:** [`stage_02_system_identification/analysis/identify_fopdt.py`](../../stage_02_system_identification/analysis/identify_fopdt.py)
* **Comparador de Puntos de Operación:** [`stage_02_system_identification/analysis/compare_operating_points.py`](../../stage_02_system_identification/analysis/compare_operating_points.py)

### Ejecución del Análisis:

```bash
cd ~/ros2-for-control-dc-motor-system/stage_02_system_identification/analysis

# Identificar modelo FOP para 45% PWM
python3 identify_fop.py ../data/raw/pwm_45/motor_step_response.csv

# Identificar modelo FOPDT para 45% PWM
python3 identify_fopdt.py ../data/raw/pwm_45/motor_step_response.csv

# Comparar respuestas en 30%, 45% y 60%
python3 compare_operating_points.py ../data/raw/pwm_30/*.csv ../data/raw/pwm_45/*.csv ../data/raw/pwm_60/*.csv
```

---

## 14. Tabla de Resultados Experimentales

Complete la tabla con los parámetros identificados en los tres ensayos:

| PWM (\%) | $\omega_{ss}$ (rad/s) | $K$ (rad/s / \%PWM) | $\tau_{\text{FOP}}$ (s) | $\theta$ (s) | $\tau_{\text{FOPDT}}$ (s) | Modelo Seleccionado |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **30 %** | | | | | | |
| **45 %** | | | | | | |
| **60 %** | | | | | | |

---

## 15. Construcción de las Funciones de Transferencia

Escriba las funciones de transferencia obtenidas para cada punto de operación:

$$G_{30}(s) = \frac{K_{30}}{\tau_{30} s + 1}$$

$$G_{45}(s) = \frac{K_{45} e^{-\theta_{45} s}}{\tau_{45} s + 1}$$

$$G_{60}(s) = \frac{K_{60}}{\tau_{60} s + 1}$$

---

## 16. Preguntas de Análisis

1. ¿Por qué el modelo experimental se formula en función del porcentaje PWM ($\Omega(s)/U_{\text{PWM}}(s)$) en lugar del voltaje analógico de armadura?
2. ¿Qué significado físico tiene el valor numérico y las unidades de la ganancia estática $K$?
3. ¿Por qué el criterio del $63.2\,\%$ es una propiedad exacta de los sistemas lineales de primer orden?
4. ¿Cómo afecta la presencia de un retardo aparente $\theta$ a la estimación de la constante de tiempo $\tau$?
5. ¿Qué limitación impone la tasa de muestreo de $10\text{ Hz}$ ($T_s = 0.1\text{ s}$) sobre la resolución para estimar $\theta$?
6. Si la ganancia $K$ varía apreciablemente entre el $30\,\%$ y el $60\,\%$, ¿qué conclusiones se derivan sobre la linealidad de la planta y la fricción seca (*Coulomb*)?
7. ¿Por qué un modelo de primer orden simplificado resulta suficiente para diseñar controladores de velocidad robustos en motores DC?

---

## 17. Criterios de Finalización y Resultado Esperado

$$\boxed{\text{Ensayos 30\%, 45\%, 60\%} \longrightarrow \text{Datos CSV} \longrightarrow \text{Parámetros } (K, \tau, \theta) \longrightarrow \text{Funciones de Transferencia } G(s)}$$

La Guía 2 culmina exitosamente cuando se dispone de la base de datos experimental, las gráficas comparativas de respuesta temporal y las funciones de transferencia identificadas, las cuales servirán de entrada para la **Guía 3 (Validación de Modelos)** y el **Diseño de Controladores PI/PID (Guía 4 y 5)**.

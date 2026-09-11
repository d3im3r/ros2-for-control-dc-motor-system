# Guía 2: Identificación Experimental Mediante Prueba Escalón

<div align="center">

**Control Inteligente — `ING01343-ING278`**  
**Politécnico Colombiano Jaime Isaza Cadavid**  
*Facultad de Ingeniería — Departamento de Electrónica*  
**Profesor:** Deimer Miranda Montoya, MSc.(c)

</div>

---

## 1. Introducción

Identificación experimental en lazo abierto de la función de transferencia del motor DC aplicando escalones de PWM al $30\,\%$, $45\,\%$ y $60\,\%$.

---

## 2. Metodología de la Prueba Escalón

El ensayo experimental estándar tiene una duración total de **40.0 segundos** ($400$ muestras registradas a $T_s = 0.1\text{ s}$ / $10\text{ Hz}$):

| Fase | Ventana de Tiempo | Entrada PWM | Propósito Experimental |
| :--- | :---: | :---: | :--- |
| **1. Reposo Inicial** | $0.0\text{ s} \le t < 1.0\text{ s}$ | $0.0\,\%$ | Validar velocidad inicial en reposo ($\omega_0 = 0$). |
| **2. Escalón Aplicado** | $1.0\text{ s} \le t < 36.0\text{ s}$ | $\text{step}\,\%$ | **35.0 s efectivos** para capturar transitorio completo y régimen permanente ($\omega_{ss}$). |
| **3. Reposo Final** | $36.0\text{ s} \le t \le 40.0\text{ s}$ | $0.0\,\%$ | Desaceleración y frenado seguro de la planta. |

### Diagrama del Perfil Temporal

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

---

## 3. Modelos Candidatos

### 3.1. Primer Orden sin Retardo (FOP)

$$G_{\text{FOP}}(s) = \frac{\Omega(s)}{U(s)} = \frac{K}{\tau s + 1}$$

### 3.2. Primer Orden con Retardo Aparente (FOPDT)

$$G_{\text{FOPDT}}(s) = \frac{\Omega(s)}{U(s)} = \frac{K e^{-\theta s}}{\tau s + 1}$$

---

## 4. Fórmulas de Cálculo Paramétrico

A partir de la curva de reacción experimental:

* **Ganancia Estática ($K$):**
  $$K = \frac{\omega_{ss} - \omega_0}{u_{ss} - u_0}\quad \left[\frac{\text{rad/s}}{\%\,\text{PWM}}\right]$$

* **Constante de Tiempo ($\tau$):**  
  Calculada mediante el criterio del $63.2\,\%$ del cambio total:
  $$\omega(t_{63.2\%}) = \omega_0 + 0.632 \cdot (\omega_{ss} - \omega_0)$$
  $$\tau = t_{63.2\%} - t_0$$

* **Retardo Aparente ($\theta$):**  
  Tiempo transcurrido desde el escalón ($t_0$) hasta el inicio de la respuesta medible:
  $$\theta \approx t_{\text{inicio}} - t_0$$

---

## 5. Implementación y Scripts en el Repositorio

### 5.1. Orquestación y Lanzamiento de Ensayos en ROS 2
Ubicación del launch: [`ros2_ws/src/dc_motor_bringup/launch/stage_02_identification.launch.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_bringup/launch/stage_02_identification.launch.py)

Generador del perfil escalón: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/step_response.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_experiments/dc_motor_experiments/step_response.py)  
Registrador de datos CSV: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py)

```bash
# Ensayo 1: Escalón al 30% PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=30.0

# Ensayo 2: Escalón al 45% PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0

# Ensayo 3: Escalón al 60% PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=60.0
```

### 5.2. Scripts de Identificación Paramétrica Offline (Python)
* Identificación FOP: [`stage_02_system_identification/analysis/identify_fop.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/stage_02_system_identification/analysis/identify_fop.py)
* Identificación FOPDT: [`stage_02_system_identification/analysis/identify_fopdt.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/stage_02_system_identification/analysis/identify_fopdt.py)
* Comparación de Puntos de Operación: [`stage_02_system_identification/analysis/compare_operating_points.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/stage_02_system_identification/analysis/compare_operating_points.py)

```bash
cd stage_02_system_identification/analysis

# Ejecutar ajuste FOP
python3 identify_fop.py ../data/raw/pwm_45/motor_step_response.csv

# Ejecutar ajuste FOPDT
python3 identify_fopdt.py ../data/raw/pwm_45/motor_step_response.csv

# Comparar curvas de reacción
python3 compare_operating_points.py ../data/raw/pwm_30/*.csv ../data/raw/pwm_45/*.csv ../data/raw/pwm_60/*.csv
```

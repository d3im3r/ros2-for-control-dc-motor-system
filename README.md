# 🚀 ros2-for-control-dc-motor-system — Control e Identificación de Motor DC en ROS 2 & micro-ROS

<p align="center">
  <img src="https://img.shields.io/badge/ROS_2-Humble_Hawksbill-22314E?logo=ros&logoColor=white" alt="ROS 2 Humble">
  <img src="https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white" alt="Ubuntu 22.04">
  <img src="https://img.shields.io/badge/ESP32-PlatformIO-orange?logo=espressif&logoColor=white" alt="PlatformIO ESP32">
  <img src="https://img.shields.io/badge/micro--ROS-Serial_115200-green" alt="micro-ROS Serial">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License">
</p>

Repositorio integral de **ROS 2 (Humble)** y firmware para **ESP32 (micro-ROS)** orientado al **diseño, instrumentación, identificación paramétrica experimental y control de velocidad en lazo cerrado** de una planta de motor DC mediante pruebas de respuesta escalón.

---

## 📑 Tabla de Contenidos

1. [🗺️ Roadmap Metodológico por Stages](#️-roadmap-metodológico-por-stages)
2. [📥 Paso 1: Descarga e Instalación del Workspace ROS 2 en el PC](#-paso-1-descarga-e-instalación-del-workspace-ros-2-en-el-pc)
3. [🔌 Paso 2: Configuración del Hardware y Firmware en el ESP32](#-paso-2-configuración-del-hardware-y-firmware-en-el-esp32)
4. [🤖 Paso 3: Conexión Serial con el micro-ROS Agent](#-paso-3-conexión-serial-con-el-micro-ros-agent)
5. [🚀 Paso 4: Ejecución Experimental por Stages](#-paso-4-ejecución-experimental-por-stages)
6. [⏱️ Perfil Temporal de la Prueba Escalón (Stage 02)](#️-perfil-temporal-de-la-prueba-escalón-stage-02)
7. [⚙️ Arquitectura de Software, Nodos y Tópicos](#️-arquitectura-de-software-nodos-y-tópicos)
8. [📊 Formato de Datos (CSV) y Modelado Matemático (FOP / FOPDT)](#-formato-de-datos-csv-y-modelado-matemático-fop--fopdt)
9. [📁 Estructura del Repositorio](#-estructura-del-repositorio)
10. [🔧 Solución de Problemas (Troubleshooting)](#-solución-de-problemas-troubleshooting)
11. [👥 Autores y Licencia](#-autores-y-licencia)

---

## 🗺️ Roadmap Metodológico por Stages

El proyecto está organizado siguiendo una metodología de control incremental y modular:

| Stage | Estado | Título | Pregunta Clave | Entregables / Archivos |
| :---: | :---: | :--- | :--- | :--- |
| **00** | <img src="https://img.shields.io/badge/Completado-brightgreen?style=flat-square" alt="Completado"> | **System Design** | *¿Cómo estructurar el sistema distribuido?* | [Guía 0](docs/guides/Inteligente_guia0.tex), arquitectura y contrato de tópicos. |
| **01** | <img src="https://img.shields.io/badge/Completado-brightgreen?style=flat-square" alt="Completado"> | **Motor Instrumentation** | *¿Puedo accionar y medir correctamente?* | [Guía 1](docs/guides/Inteligente_guia1.tex), calibración ($N_{rev}=960$), bringup Stage 01. |
| **02** | <img src="https://img.shields.io/badge/En_Progreso-orange?style=flat-square" alt="En Progreso"> | **System Identification** | *¿Qué modelo describe la dinámica del motor?* | [Guía 2](docs/guides/Inteligente_guia2.tex), curvas de reacción ($30\%, 45\%, 60\%$), modelos FOP y FOPDT. |
| **03** | <img src="https://img.shields.io/badge/Pendiente-lightgrey?style=flat-square" alt="Pendiente"> | **Model Validation** | *¿El modelo predice datos no ensayados?* | Métricas RMSE/MAE, ajuste porcentual FIT y modelo nominal. |
| **04** | <img src="https://img.shields.io/badge/Pendiente-lightgrey?style=flat-square" alt="Pendiente"> | **Controller Design** | *¿Qué controlador cumple los requerimientos?* | Diseño PI/PID/Inteligente y simulación dinámica. |
| **05** | <img src="https://img.shields.io/badge/Pendiente-lightgrey?style=flat-square" alt="Pendiente"> | **Closed-Loop Control** | *¿El lazo cerrado físico responde adecuadamente?* | Validación experimental en tiempo real y rechazo a perturbaciones. |

---

## 📥 Paso 1: Descarga e Instalación del Workspace ROS 2 en el PC

Sigue estos pasos en tu terminal de Ubuntu / Pop!_OS para clonar y compilar el espacio de trabajo:

### 1.1. Clonar el repositorio
```bash
git clone https://github.com/d3im3r/ros2-for-control-dc-motor-system.git
cd ros2-for-control-dc-motor-system
```

### 1.2. Instalar dependencias del sistema
```bash
sudo apt update
sudo apt install -y python3-matplotlib python3-pip python3-numpy python3-scipy python3-colcon-common-extensions ros-humble-micro-ros-agent
```

### 1.3. Compilar los paquetes de ROS 2
```bash
cd ros2_ws
colcon build --symlink-install
```

### 1.4. Cargar el entorno (*Sourcing*)
```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

> 💡 **Tip:** Para cargar el entorno automáticamente en cada nueva terminal:
> ```bash
> echo "source /home/$USER/ros2-for-control-dc-motor-system/ros2_ws/install/setup.bash" >> ~/.bashrc
> ```

---

## 🔌 Paso 2: Configuración del Hardware y Firmware en el ESP32

El firmware micro-ROS corre sobre el microcontrolador ESP32 y se encarga de la interacción directa con el hardware a través de interrupciones, timers y modulación LEDC.

### 2.1. Conexiones de Hardware y Pines

| Componente | Función | Pin ESP32 | Descripción |
| :--- | :--- | :---: | :--- |
| **Encoder Canal A** | Entrada pulsos A | `GPIO 32` | Interrupción de hardware (`CHANGE`) |
| **Encoder Canal B** | Entrada pulsos B | `GPIO 33` | Determinación de sentido de giro |
| **Puente H L298N** | PWM Canal B (`ENB`) | `GPIO 25` | Modulación LEDC ($500\text{ Hz}$, $8\text{ bits}$, $0-255$) |
| **Puente H L298N** | Sentido de giro (`IN3`) | `GPIO 27` | Nivel lógico de dirección |
| **Puente H L298N** | Sentido de giro (`IN4`) | `GPIO 26` | Nivel lógico de dirección |
| **Display OLED SH1106** | $I^2C$ SDA | `GPIO 21` | Línea de datos OLED ($128\times 64$) |
| **Display OLED SH1106** | $I^2C$ SCL | `GPIO 22` | Línea de reloj OLED |

> ⚙️ **Calibración Experimental del Encoder:** $N_{\mathrm{rev}} = 960\ \text{ticks/rev}$.

### 2.2. Configuración en PlatformIO (`platformio.ini`)

```ini
[env:esp32dev]
platform = espressif32@6.5.0
board = esp32dev
framework = arduino

monitor_speed = 115200

board_microros_distro = humble
board_microros_transport = serial

lib_deps =
    https://github.com/micro-ROS/micro_ros_platformio
    adafruit/Adafruit GFX Library
    adafruit/Adafruit SH110X

build_flags =
    -DCORE_DEBUG_LEVEL=0
```

---

## 🤖 Paso 3: Conexión Serial con el micro-ROS Agent

Una vez cargado el firmware en el ESP32 y conectado mediante el cable USB al PC:

### 3.1. Asignar permisos al puerto serial
```bash
sudo chmod 666 /dev/ttyUSB0
# o añadir tu usuario al grupo dialout:
sudo usermod -a -G dialout $USER
```
*(Si tu dispositivo aparece como `/dev/ttyACM0`, usa ese puerto).*

### 3.2. Iniciar el Agente micro-ROS por Serial (115200 baudios)
```bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200
```

### 3.3. Verificar la comunicación
En otra terminal, comprueba que el nodo y los tópicos estén activos:
```bash
ros2 node list
# Debe mostrar: /motor_step_node

ros2 topic list
# Debe mostrar: /pwm_input, /vel_rad_s, /vel_rpm

ros2 topic hz /vel_rad_s
# Debe reportar una frecuencia estable de ~10 Hz (Ts = 0.1 s)
```

---

## 🚀 Paso 4: Ejecución Experimental por Stages

### 4.1. Stage 01: Instrumentación y Validación de la Planta

Verifica la respuesta del motor y la consistencia de los tópicos:
```bash
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```

### 4.2. Stage 02: Pruebas Escalón Automatizadas (Identificación)

El launch de Stage 02 inicia en simultáneo: el generador de perfil temporal, el registrador de datos CSV y el monitor visual interactivo con Matplotlib:

```bash
# Ensayo 1: Escalón del 30 % PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=30.0

# Ensayo 2: Escalón del 45 % PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0

# Ensayo 3: Escalón del 60 % PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=60.0
```

> **Parámetros configurables del Launch:**
> - `step`: Amplitud del escalón en porcentaje `[-100.0, 100.0]`. Por defecto: `0.0`.
> - `total_time`: Duración total de la prueba en segundos. Por defecto: `40.0`.

---

## ⏱️ Perfil Temporal de la Prueba Escalón (Stage 02)

El ciclo de prueba estándar está configurado para una captura total de **40.0 segundos (400 muestras a 10 Hz)**:

| Fase | Intervalo de Tiempo | PWM (\%) | Propósito |
| :--- | :---: | :---: | :--- |
| **1. Reposo Inicial** | `0.0 s` a `1.0 s` | `0.0 %` | Registrar la condición inicial y validar estabilidad en reposo ($\omega_0$). |
| **2. Escalón Aplicado** | `1.0 s` a `36.0 s` | `step %` | **35.0 s efectivos** para capturar transitorio completo y régimen permanente ($\omega_{ss}$). |
| **3. Reposo Final** | `36.0 s` a `40.0 s` | `0.0 %` | Desaceleración y frenado seguro del motor. |

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

## ⚙️ Arquitectura de Software, Nodos y Tópicos

```text
                   +---------------------+
                   |  step_profile_node  | (dc_motor_experiments)
                   +----------+----------+
                              | /pwm_input (Float32, %)
                              v
                   +---------------------+
                   |   motor_step_node   | (ESP32 / micro-ROS)
                   +----------+----------+
                              | /vel_rad_s (Float32, rad/s)
               +--------------+--------------+
               |                             |
               v                             v
    +--------------------+       +------------------------+
    |  step_response_db  |       |  step_response_graph   |
    |     (CSV Logger)   |       |  (Gráfica tiempo real) |
    +--------------------+       +------------------------+
```

### Contrato de Tópicos

* `/pwm_input` (`std_msgs/msg/Float32`): Comando de entrada al puente H ($-100.0$ a $100.0\,\%$).
* `/vel_rad_s` (`std_msgs/msg/Float32`): Velocidad angular estimada por el encoder en $\text{rad/s}$ ($T_s = 0.1\text{ s}$).
* `/vel_rpm` (`std_msgs/msg/Float32`): Velocidad angular en $\text{rpm}$ para visualización local y remota.

---

## 📊 Formato de Datos (CSV) y Modelado Matemático (FOP / FOPDT)

Cada ejecución de `data_logger` genera un archivo con formato:

`motor_step_response_YYYYMMDD_HHMMSS.csv`

```csv
Time (s),Angular Velocity (rad/s),PWM (%)
0.100,0.000000,0.000
0.200,0.000000,0.000
...
1.100,2.152431,45.000
...
36.100,45.892100,0.000
```

### Modelado Matemático

A partir de los datos registrados se identifican las funciones de transferencia:

$$G_{\text{FOP}}(s) = \frac{K}{\tau s + 1} \qquad \text{o} \qquad G_{\text{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$$

donde:

* **Ganancia estática:** $K = \frac{\omega_{ss} - \omega_0}{u_{ss} - u_0}\quad [\text{rad/s / \%PWM}]$
* **Constante de tiempo:** $\tau = t_{63.2\%} - t_0$ (criterio del $63.2\,\%$ de la respuesta total).
* **Retardo aparente:** $\theta \approx t_{\text{inicio}} - t_0$.

### Scripts de Ajuste Paramétrico Offline

```bash
cd stage_02_system_identification/analysis

# Identificación Primer Orden (FOP)
python3 identify_fop.py ../data/raw/pwm_45/motor_step_response.csv

# Identificación con Retardo (FOPDT)
python3 identify_fopdt.py ../data/raw/pwm_45/motor_step_response.csv

# Comparar Puntos de Operación (30%, 45%, 60%)
python3 compare_operating_points.py ../data/raw/pwm_30/*.csv ../data/raw/pwm_45/*.csv ../data/raw/pwm_60/*.csv
```

---

## 📁 Estructura del Repositorio

```text
ros2-for-control-dc-motor-system/
├── README.md                            # Presentación y documentación general
├── LICENSE                              # Licencia Apache-2.0
├── .gitignore                           # Reglas de exclusión de Git
│
├── docs/                                # Documentación académica y guías
│   ├── guides/                          # Guías en LaTeX (Inteligente_guia0, 1, 2)
│   ├── diagrams/                        # Diagramas de arquitectura
│   └── images/                          # Recursos gráficos
│
├── ros2_ws/                             # Espacio de Trabajo ROS 2 (Software Ejecutable)
│   └── src/
│       ├── dc_motor_bringup/            # Paquete de launch files y orquestación
│       │   └── launch/
│       │       ├── motor_system.launch.py
│       │       ├── stage_01_instrumentation.launch.py
│       │       ├── stage_02_identification.launch.py
│       │       ├── stage_03_validation.launch.py
│       │       ├── stage_04_control.launch.py
│       │       └── stage_05_closed_loop.launch.py
│       │
│       ├── dc_motor_experiments/        # Paquete de adquisición y visualización
│       │   └── dc_motor_experiments/
│       │       ├── step_response.py     # Generador de perfil escalón
│       │       ├── data_logger.py       # Registrador CSV
│       │       └── velocity_monitor.py  # Monitor gráfico tiempo real
│       │
│       └── dc_motor_control/            # Paquete de controladores (PI, PID, etc.)
│           └── dc_motor_control/
│               ├── pi_controller.py
│               └── pid_controller.py
│
├── stage_00_system_design/              # Diseño de arquitectura y especificaciones
├── stage_01_motor_instrumentation/      # Calibración del encoder (960 ticks/rev)
├── stage_02_system_identification/      # Datos CSV (raw/processed) y análisis FOP/FOPDT
│   ├── data/raw/                        # Ensayos a 30%, 45% y 60%
│   ├── analysis/                        # Scripts de identificación matemática
│   └── models/                          # Parámetros K, tau y theta
├── stage_03_model_validation/           # Validación del modelo
├── stage_04_controller_design/          # Diseño de controladores
└── stage_05_closed_loop_control/        # Ensayos en lazo cerrado
```

---

## 🔧 Solución de Problemas (Troubleshooting)

| Problema | Causa Posible | Solución |
| :--- | :--- | :--- |
| `Package 'dc_motor_bringup' not found` | No se ha ejecutado el `source` | Ejecuta `source ~/ros2-for-control-dc-motor-system/ros2_ws/install/setup.bash` en la terminal. |
| `No module named 'matplotlib'` | Falta instalar librerías de Python en Ubuntu | Ejecuta `sudo apt install -y python3-matplotlib python3-scipy python3-numpy`. |
| Error al abrir `/dev/ttyUSB0` | Permisos insuficientes en el puerto serie | Ejecuta `sudo chmod 666 /dev/ttyUSB0` o agrega tu usuario con `sudo usermod -a -G dialout $USER`. |
| La gráfica no recibe datos | El micro-ROS Agent no está en ejecución | Inicia el agente: `ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200`. |
| El motor no gira en el launch | El valor por defecto es `step:=0.0` | Especifica el porcentaje del escalón en el comando: `step:=45.0`. |

---

## 👥 Autores y Licencia

* **Deimer Miranda Montoya, MSc.(c)** — `demiranda@unal.edu.co` / `deimer_miranda91162@elpoli.edu.co`
* **Institución:** [Politécnico Colombiano Jaime Isaza Cadavid](https://www.politecnicojic.edu.co/) — Facultad de Ingeniería
* **Asignatura:** Control Inteligente (`ING01343-ING278`)
* **Licencia:** [Apache License 2.0](LICENSE)

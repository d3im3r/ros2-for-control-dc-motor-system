# ROS 2 for DC Motor Control System

Este repositorio contiene la infraestructura completa de control e instrumentación basada en **ROS 2 Humble** y **micro-ROS** (ESP32) para un motor DC con encoder de cuadratura accionado mediante un puente H L298.

El desarrollo sigue una metodología experimental incremental dividida en **Stages**, desacoplando el código de firmware, nodos de adquisición, identificación matemática y controladores.

---

## 🏗️ Arquitectura General

```text
┌─────────────────────────────────────────────────────────────┐
│                      Computador (ROS 2)                     │
│                                                             │
│  [dc_motor_experiments]        [dc_motor_control]           │
│  • step_response               • pi_controller              │
│  • data_logger                 • pid_controller             │
│  • velocity_monitor                                         │
│          ▲                              │                   │
│          │ /vel_rad_s                   │ /pwm_input        │
│          │ /vel_rpm                     │ (Float32, %)      │
│          └──────────────┬───────────────┘                   │
│                         ▼                                   │
│                 [micro_ros_agent]                           │
└─────────────────────────┬───────────────────────────────────┘
                          │ Serial USB (115200 baud)
┌─────────────────────────▼───────────────────────────────────┐
│                      ESP32 (micro-ROS)                      │
│                                                             │
│  [motor_step_node]                                          │
│  • ISR Encoder (Canal A / B) ──► Nrev = 960 ticks/rev       │
│  • Timer 10 Hz (Ts = 0.1 s) ──► rad/s, rpm                  │
│  • PWM LEDC (500 Hz, 8 bits) ──► IN3, IN4, ENB              │
│  • OLED Display SH1106 (I2C)                                │
└──────────────┬──────────────────────────────┬───────────────┘
               │ PWM (ENA/ENB, IN1-IN4)       ▲ Pulsos A / B
               ▼                              │
         ┌───────────┐                  ┌───────────┐
         │   L298    │ ─── Potencia ──► │  Motor DC │
         │ (Puente H)│                  │ + Encoder │
         └───────────┘                  └───────────┘
```

---

## ⚙️ Hardware y Software Utilizado

### Hardware
* **Microcontrolador:** ESP32 NodeMCU-32S.
* **Driver de Potencia:** Puente H L298N (Canal B: `ENB` GPIO 25, `IN3` GPIO 27, `IN4` GPIO 26).
* **Motor & Encoder:** Motor DC Pololu con encoder incremental de cuadratura (`ENCA` GPIO 32, `ENCB` GPIO 33).
* **Display Local:** Pantalla OLED SH1106 $128\times64$ $I^2C$ (`SDA` GPIO 21, `SCL` GPIO 22).

### Software
* **Sistema Operativo:** Linux / Pop!_OS / Ubuntu 22.04 LTS.
* **Middleware Robótico:** ROS 2 Humble Hawksbill.
* **Integración Embebida:** micro-ROS (cliente C/C++ en ESP32, agente serial en PC).
* **Procesamiento de Datos:** Python 3, NumPy, SciPy, Matplotlib.

---

## 🗺️ Roadmap de Desarrollo por Stages

| Etapa | Estado | Nombre del Stage | Descripción |
| :--- | :---: | :--- | :--- |
| **Stage 00** | ✅ | **System Design** | Arquitectura conceptual, división microcontrolador/PC y contrato de tópicos. |
| **Stage 01** | ✅ | **Motor Instrumentation** | Firmware ESP32, conteo de ticks ($N_{rev}=960$), PWM LEDC, display OLED y bringup base. |
| **Stage 02** | 🚧 | **System Identification** | Pruebas escalón ($30\%, 45\%, 60\%$), captura de curvas de reacción y modelos FOP/FOPDT. |
| **Stage 03** | ⏳ | **Model Validation** | Validación cruzada del modelo identificado frente a nuevas señales de excitación. |
| **Stage 04** | ⏳ | **Controller Design** | Síntesis y ajuste de controladores de velocidad (P, PI, PID, Inteligente). |
| **Stage 05** | ⏳ | **Closed-Loop Control** | Implementación y verificación del lazo cerrado en la planta física real. |

---

## 📦 Estructura del Repositorio

```text
ros2-for-control-dc-motor-system/
├── README.md
├── LICENSE
├── docs/
│   ├── guides/                      # Guías académicas de laboratorio en LaTeX
│   ├── diagrams/                    # Diagramas de flujo y arquitectura
│   └── images/                      # Capturas y recursos gráficos
├── ros2_ws/                         # Workspace de ROS 2
│   └── src/
│       ├── dc_motor_bringup/        # Paquete de launch files y orquestación
│       ├── dc_motor_experiments/    # Nodos de excitación, logging y monitoreo
│       └── dc_motor_control/        # Nodos de controladores (PI, PID, etc.)
├── stage_00_system_design/          # Documentación de diseño y arquitectura
├── stage_01_motor_instrumentation/  # Calibración de encoder e instrumentación
├── stage_02_system_identification/  # Adquisición de datos y análisis FOP/FOPDT
├── stage_03_model_validation/       # Validación de modelos identificados
├── stage_04_controller_design/      # Diseño y sintonización de control
└── stage_05_closed_loop_control/    # Ensayos experimentales en lazo cerrado
```

---

## 🚀 Guía de Inicio Rápido

1. **Compilar el workspace de ROS 2:**
   ```bash
   cd ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ```

2. **Lanzar la etapa correspondiente (ej. Stage 01):**
   ```bash
   ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
   ```

3. **Lanzar prueba escalón automática (ej. Stage 02 a 45% PWM):**
   ```bash
   ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0
   ```

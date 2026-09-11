# Stage 01: Motor Instrumentation

<div align="center">

<img src="https://img.shields.io/badge/Stage-01-blue?style=for-the-badge" alt="Stage 01">
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" alt="Completed">
<img src="https://img.shields.io/badge/Focus-Firmware_%26_Instrumentation-purple?style=for-the-badge" alt="Instrumentation">

</div>

---

## 🎯 Guiding Question
> **Can I apply a known actuation to the motor and measure its dynamic response accurately?**

---

## 📌 Objectives

1. **Experimental Encoder Calibration:** Accurately determine the effective counts per revolution ($N_{\mathrm{rev}} = 960\ \text{ticks/rev}$) through multi-trial physical calibration.
2. **Real-Time Firmware Implementation:** Develop the `motor_step_node` for the ESP32 using the micro-ROS framework in C++.
3. **LEDC Peripheral PWM Modulation:** Configure hardware PWM generation at $500\text{ Hz}$ with 8-bit resolution ($0\text{--}255$) coupled to an L298N dual H-Bridge.
4. **Discrete Velocity Estimation:** Implement periodic sampling at $10\text{ Hz}$ ($T_s = 0.1\text{ s}$) to compute angular velocity in $\text{rad/s}$ and $\text{rpm}$ from interrupt tick deltas.
5. **Local Telemetry Display:** Drive an SH1106 OLED display ($128\times 64$) over $I^2C$ to visualize real-time PWM, velocity, and connection state.
6. **Bidirectional ROS 2 Validation:** Verify real-time command reception on `/pwm_input` and telemetry publishing on `/vel_rad_s` and `/vel_rpm`.

---

## 🧮 Theoretical & Mathematical Formulation

### 1. Discrete Velocity Estimation
At each sampling instant $t_k = k \cdot T_s$ ($T_s = 0.1\text{ s}$), the timer callback calculates the tick variation $\Delta N_k = N(t_k) - N(t_{k-1})$:

$$\Delta \theta_k = \frac{\Delta N_k}{N_{\mathrm{rev}}} \cdot 2\pi \quad [\text{rad}]$$

$$\omega_k = \frac{\Delta \theta_k}{T_s} = \frac{2\pi \cdot \Delta N_k}{N_{\mathrm{rev}} \cdot T_s} \quad [\text{rad/s}]$$

$$\omega_{\mathrm{rpm}, k} = \omega_k \cdot \frac{60}{2\pi} = \frac{60 \cdot \Delta N_k}{N_{\mathrm{rev}} \cdot T_s} \quad [\text{rpm}]$$

With $N_{\mathrm{rev}} = 960$ and $T_s = 0.1\text{ s}$:
$$\omega_k = \frac{2\pi \cdot \Delta N_k}{96} \approx 0.06545 \cdot \Delta N_k \quad [\text{rad/s}]$$

### 2. PWM Actuation Mapping
Given an input percentage command $u \in [-100.0, 100.0]\,\%$, the 8-bit duty cycle ($0\text{--}255$) and direction logic are computed as:

$$\text{duty\_raw} = \text{round}\left( \frac{\lvert u \rvert}{100.0} \cdot 255 \right)$$

$$\text{Direction} = \begin{cases} \text{Forward (IN3=HIGH, IN4=LOW)}, & u > 0 \\ \text{Reverse (IN3=LOW, IN4=HIGH)}, & u < 0 \\ \text{Brake / Stop (IN3=LOW, IN4=LOW)}, & u = 0 \end{cases}$$

---

## 🔌 Hardware & Pinout Setup

| Signal | ESP32 GPIO | Connected Component | Role / Configuration |
| :--- | :---: | :--- | :--- |
| `ENCA` | `GPIO 32` | Encoder Ch A | Hardware Interrupt (`attachInterrupt(..., CHANGE)`) |
| `ENCB` | `GPIO 33` | Encoder Ch B | Quadrature direction sensing |
| `ENB` | `GPIO 25` | L298N Enable B | LEDC PWM (500 Hz, 8-bit resolution, Channel 0) |
| `IN3` | `GPIO 27` | L298N Input 3 | Direction logic level |
| `IN4` | `GPIO 26` | L298N Input 4 | Direction logic level |
| `SDA` | `GPIO 21` | SH1106 OLED | $I^2C$ Data |
| `SCL` | `GPIO 22` | SH1106 OLED | $I^2C$ Clock |

---

## 🔬 Experimental Calibration

The encoder calibration experiment verified ticks per output shaft revolution across 5 repeated physical trials:

| Trial | Measured Ticks ($\lvert N_i \rvert$) |
| :---: | :---: |
| 1 | 960 |
| 2 | 960 |
| 3 | 960 |
| 4 | 960 |
| 5 | 960 |

Detailed steps are documented in [encoder_calibration.md](file:///home/d3im3r/ros2-for-control-dc-motor-system/stage_01_motor_instrumentation/calibration/encoder_calibration.md).

---

## 🚀 Execution & Verification

### 1. Build and Flash Firmware
Open the project in VS Code with PlatformIO (or use CLI) pointing to [`firmware/esp32_motor_step`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step):
```bash
cd firmware/esp32_motor_step
pio run -t upload
```

### 2. Launch ROS 2 Instrumentation Pipeline
```bash
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```
This launch file starts:
* `micro_ros_agent` serial connection on `/dev/ttyUSB0` at `115200 baud`.
* `velocity_monitor` real-time dynamic plotter.

### 3. Manual Actuation Test
In a separate terminal, apply a step PWM command:
```bash
# Apply 40% forward PWM
ros2 topic pub --once /pwm_input std_msgs/msg/Float32 "{data: 40.0}"

# Echo estimated velocity
ros2 topic echo /vel_rad_s

# Stop motor
ros2 topic pub --once /pwm_input std_msgs/msg/Float32 "{data: 0.0}"
```

---

## 📁 Directory Organization

```text
stage_01_motor_instrumentation/
├── README.md                            # Stage 01 presentation and overview
├── calibration/                         # Encoder calibration protocol and results
│   ├── encoder_calibration.md
│   └── results/
│       └── README.md
├── plots/                               # Instrumentation & response validation plots
│   └── README.md
└── results/                             # Logged validation metrics and datasets
    └── README.md
```

---

## 📖 Associated Academic Guide

For the complete theoretical derivation, step-by-step firmware breakdown, and oscilloscope validation:
* **[Guide 1: Motor Instrumentation and Calibration](../docs/guides/Inteligente_guia1.md)**

---

## ⏭️ Next Step

Proceed to **[Stage 02: System Identification](../stage_02_system_identification/README.md)** to conduct open-loop step tests at $30\%$, $45\%$, and $60\%$ PWM, log temporal datasets, and compute transfer function models ($G_{\mathrm{FOP}}$ and $G_{\mathrm{FOPDT}}$).

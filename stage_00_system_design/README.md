# Stage 00: System Design

<div align="center">

<img src="https://img.shields.io/badge/Stage-00-blue?style=for-the-badge" alt="Stage 00">
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" alt="Completed">
<img src="https://img.shields.io/badge/Target-Architecture_%26_Interfaces-purple?style=for-the-badge" alt="Architecture">

</div>

---

## 🎯 Guiding Question
> **How should the distributed system be architected to actuate the motor and observe its dynamic behavior reliably?**

---

## 📌 Objectives

1. **Distributed System Architecture:** Establish clear boundaries and responsibilities between the host computer (ROS 2 Humble) and the real-time microcontroller (ESP32 / micro-ROS).
2. **Interface Specification:** Formalize the communication contract (topics, datatypes, frequencies, and engineering units).
3. **Hardware & Electrical Pinout:** Define the pin assignments for motor PWM, H-Bridge logic levels, encoder interrupts, and the $I^2C$ telemetry display.
4. **Foundational Readiness:** Lay the groundwork for reproducible step-response experiments and closed-loop control.

---

## 🏗️ System Architecture & Topology

```mermaid
flowchart LR
    subgraph PC ["Host Computer (ROS 2 Humble / Linux)"]
        AGENT(["micro_ros_agent<br>(Serial 115200)"])
        LOGGER(["data_logger.py<br>(CSV Logger)"])
        MONITOR(["velocity_monitor.py<br>(Real-time Plotter)"])
        LAUNCH(["dc_motor_bringup<br>(Launch Files)"])
    end

    subgraph MCU ["Microcontroller (ESP32 / micro-ROS)"]
        NODE(["motor_step_node"])
        LEDC["LEDC Peripheral<br>(500 Hz, 8-bit)"]
        ISR["Encoder ISR<br>(CHANGE, GPIO 32)"]
    end

    subgraph HW ["Physical Plant & Power Hardware"]
        DRIVER["L298N H-Bridge"]
        MOTOR["DC Motor + Gearbox"]
        ENCODER["Quadrature Encoder"]
        OLED["SH1106 OLED (128x64)"]
    end

    LAUNCH -.->|Orchestrates| AGENT
    AGENT <===>|USB Serial /dev/ttyUSB0| NODE
    NODE -->|PWM + Dir| LEDC --> DRIVER -->|Power| MOTOR
    MOTOR -->|Rotation| ENCODER -->|A/B Pulses| ISR --> NODE
    NODE -->|I2C SDA/SCL| OLED
    NODE ===>|/vel_rad_s, /vel_rpm| AGENT
    AGENT ===> LOGGER
    AGENT ===> MONITOR
```

---

## 📐 Topic Contract and Interfaces

| Topic | Direction (rel. to ESP32) | Message Type | Rate | Units / Range | Purpose |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `/pwm_input` | Input | `std_msgs/msg/Float32` | Asynchronous | $[-100.0, 100.0]\,\%$ | Signed PWM command applied to L298N driver |
| `/vel_rad_s` | Output | `std_msgs/msg/Float32` | $10\text{ Hz}$ | $\text{rad/s}$ | Estimated shaft angular velocity |
| `/vel_rpm` | Output | `std_msgs/msg/Float32` | $10\text{ Hz}$ | $\text{rpm}$ | Estimated shaft angular velocity |

---

## 🔌 Hardware Pinout Allocation

| ESP32 Pin | Signal | Hardware Module | Function / Configuration |
| :---: | :---: | :---: | :--- |
| `GPIO 32` | `ENCA` | Encoder Channel A | Hardware interrupt input (`CHANGE`) |
| `GPIO 33` | `ENCB` | Encoder Channel B | Direction sensing logic level |
| `GPIO 25` | `ENB` | L298N H-Bridge | PWM modulation (LEDC Channel 0, 500 Hz, 8-bit) |
| `GPIO 27` | `IN3` | L298N H-Bridge | Direction control logic level |
| `GPIO 26` | `IN4` | L298N H-Bridge | Direction control logic level |
| `GPIO 21` | `SDA` | SH1106 OLED | $I^2C$ Data line |
| `GPIO 22` | `SCL` | SH1106 OLED | $I^2C$ Clock line |

---

## 📁 Directory Organization

```text
stage_00_system_design/
├── README.md                            # Stage 00 presentation and specifications
├── architecture/                        # System block diagrams and interface definitions
│   └── README.md
└── results/                             # System design deliverables and schemas
    └── README.md
```

---

## 📖 Associated Academic Guide

For in-depth mathematical derivations and design rationale, refer to:
* **[Guide 0: Design of a micro-ROS Node for a DC Motor](../docs/guides/Inteligente_guia0.md)**

---

## ⏭️ Next Step

Proceed to **[Stage 01: Motor Instrumentation](../stage_01_motor_instrumentation/README.md)** to calibrate the encoder, flash the micro-ROS firmware, and validate hardware actuation.

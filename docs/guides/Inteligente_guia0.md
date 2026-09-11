# Guía 0: Diseño de un Nodo micro-ROS para Motor DC

<div align="center">

**Control Inteligente — `ING01343-ING278`**  
**Politécnico Colombiano Jaime Isaza Cadavid**  
*Facultad de Ingeniería — Departamento de Electrónica*  
**Profesor:** Deimer Miranda Montoya, MSc.(c)

</div>

---

## 1. Introducción

En esta práctica se diseña e implementa la arquitectura conceptual de un nodo **micro-ROS** sobre un microcontrolador **ESP32** para interactuar con un motor DC Pololu, utilizando un puente H L298N y un encoder incremental de cuadratura.

---

## 2. Arquitectura del Sistema

La arquitectura distribuida se compone de dos dominios principales:

* **ESP32 (micro-ROS):** 
  * Nodo: `motor_step_node`.
  * Recepción de comando PWM en el tópico `/pwm_input`.
  * Cálculo y estimación periódica de velocidades angulares.
  * Publicación de telemetría en los tópicos `/vel_rad_s` y `/vel_rpm`.
  * Ubicación del código fuente: [`firmware/esp32_motor_step/src/main.cpp`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step/src/main.cpp)
  * Configuración de PlatformIO: [`firmware/esp32_motor_step/platformio.ini`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step/platformio.ini)

* **PC (ROS 2 Humble):** 
  * Agente de comunicación serial: `micro_ros_agent` (ejecutado a $115200\text{ baudios}$ sobre `/dev/ttyUSB0`).
  * Nodo generador de perfiles de prueba: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/step_response.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_experiments/dc_motor_experiments/step_response.py).
  * Nodo de adquisición y base de datos CSV: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_experiments/dc_motor_experiments/data_logger.py).
  * Nodo de visualización gráfica en tiempo real: [`ros2_ws/src/dc_motor_experiments/dc_motor_experiments/velocity_monitor.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_experiments/dc_motor_experiments/velocity_monitor.py).
  * Launch de orquestación general: [`ros2_ws/src/dc_motor_bringup/launch/motor_system.launch.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_bringup/launch/motor_system.launch.py).

### Diagrama de Bloques de la Arquitectura

```text
  +-------------------------------------------------------------------------+
  |                               PC (ROS 2)                                |
  |                                                                         |
  |  +---------------------+      /pwm_input       +---------------------+  |
  |  |  step_profile_node  | --------------------> |                     |  |
  |  +---------------------+                       |                     |  |
  |                                                |   micro_ros_agent   |  |
  |  +---------------------+      /vel_rad_s       |   (Serial 115200)   |  |
  |  |   data_logger_node  | <-------------------- |                     |  |
  |  +---------------------+                       +----------+----------+  |
  |                                                           |             |
  |  +---------------------+      /vel_rad_s                  |             |
  |  | velocity_monitor    | <--------------------------------+             |
  |  +---------------------+                                                |
  +-----------------------------------------------------------|-------------+
                                                              | USB / UART
  +-----------------------------------------------------------|-------------+
  |                           ESP32 (micro-ROS)               v             |
  |                                                +---------------------+  |
  |                                                |   motor_step_node   |  |
  |                                                +----------+----------+  |
  |                                                           |             |
  |               +-----------------------+-------------------+             |
  |               | Interrupción Encoder  | LEDC PWM (500 Hz) | I2C OLED    |
  |               v                       v                   v             |
  |          [Encoder A/B]          [Puente H L298N]     [Display SH1106]   |
  +-------------------------------------------------------------------------+
```

---

## 3. Contrato de Interfaces (Tópicos ROS 2)

El contrato formal de interfaces define los tópicos, direcciones de comunicación, tipos de datos estándar de ROS 2 y rangos de operación:

| Tópico | Dirección | Tipo de Mensaje | Rango / Unidades | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `/pwm_input` | Entrada (PC $\to$ ESP32) | `std_msgs/msg/Float32` | $[-100.0, 100.0]\,\%$ | Comando de ciclo de trabajo hacia el puente H L298N. |
| `/vel_rad_s` | Salida (ESP32 $\to$ PC) | `std_msgs/msg/Float32` | $\text{rad/s}$ | Velocidad angular estimada por el encoder ($T_s = 0.1\text{ s}$). |
| `/vel_rpm` | Salida (ESP32 $\to$ PC) | `std_msgs/msg/Float32` | $\text{rpm}$ | Velocidad angular estimada en revoluciones por minuto. |

---

## 4. Implementación y Código en el Repositorio

### 4.1. Suscripciones y Publicaciones micro-ROS en ESP32
Ubicación: [`firmware/esp32_motor_step/src/main.cpp`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step/src/main.cpp)

```cpp
// Declaración de suscriptores y publicadores micro-ROS
rcl_subscription_t sub_pwm_input;
rcl_publisher_t pub_vel_rad_s;
rcl_publisher_t pub_vel_rpm;

// Callback de recepción de comando PWM
void pwm_callback(const void *msgin) {
  const std_msgs__msg__Float32 *msg = (const std_msgs__msg__Float32 *)msgin;
  aplicarPWM(msg->data);
}
```

### 4.2. Ejecución del Agente micro-ROS en el PC
```bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200
```

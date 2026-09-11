# Stage 00: System Design

## 🎯 Pregunta Orientadora
> **¿Cómo debe construirse el sistema para poder actuar sobre el motor y observar su comportamiento?**

---

## 📌 Objetivos
1. Definir la arquitectura distribuida entre microcontrolador (ESP32) y computador de control (ROS 2).
2. Establecer el contrato formal de comunicación (tópicos, tipos de datos, rangos y unidades).
3. Asignar responsabilidades a cada componente físico y de software.

---

## 📐 Contrato de Tópicos e Interfaces

| Tópico | Respecto a ESP32 | Mensaje ROS 2 | Unidad | Propósito |
| :--- | :--- | :--- | :--- | :--- |
| `/pwm_input` | Entrada | `std_msgs/msg/Float32` | % ($-100$ a $+100$) | Acción de control aplicada al puente H |
| `/vel_rad_s` | Salida | `std_msgs/msg/Float32` | rad/s | Velocidad angular estimada para control |
| `/vel_rpm` | Salida | `std_msgs/msg/Float32` | rpm | Velocidad angular para monitoreo visual |

---

## 🔌 Asignación de Pines de Hardware

| GPIO ESP32 | Señal | Componente | Descripción |
| :---: | :---: | :---: | :--- |
| **32** | ENCA | Encoder | Canal A con interrupción (`CHANGE`) |
| **33** | ENCB | Encoder | Canal B de sentido |
| **25** | ENB | Puente H L298 | Entrada PWM canal B (LEDC) |
| **27** | IN3 | Puente H L298 | Sentido de giro |
| **26** | IN4 | Puente H L298 | Sentido de giro |
| **21** | SDA | Display OLED | Línea de datos $I^2C$ |
| **22** | SCL | Display OLED | Línea de reloj $I^2C$ |

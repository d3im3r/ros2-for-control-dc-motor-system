# Guía 1: Nodo micro-ROS para Motor DC

<div align="center">

**Control Inteligente — `ING01343-ING278`**  
**Politécnico Colombiano Jaime Isaza Cadavid**  
*Facultad de Ingeniería — Departamento de Electrónica*  
**Profesor:** Deimer Miranda Montoya, MSc.(c)

</div>

---

## 1. Introducción

Construcción y validación de la instrumentación física y software del motor DC utilizando **micro-ROS** sobre **ESP32**, puente H L298N, encoder de cuadratura ($N_{\text{rev}} = 960\ \text{ticks/rev}$) y display OLED SH1106.

---

## 2. Conexiones de Hardware y Pines

La siguiente tabla detalla la distribución de conexiones físicas entre el ESP32, el puente H, el encoder y la pantalla OLED:

| Componente | Función | Pin ESP32 | Descripción / Configuración |
| :--- | :--- | :---: | :--- |
| **Encoder Canal A** | Entrada pulsos A | `GPIO 32` | Interrupción de hardware (`CHANGE`, `INPUT_PULLUP`) |
| **Encoder Canal B** | Entrada pulsos B | `GPIO 33` | Determinación de sentido de giro (`INPUT_PULLUP`) |
| **Puente H L298N** | PWM Canal B (`ENB`) | `GPIO 25` | Modulación LEDC ($500\text{ Hz}$, $8\text{ bits}$, canal 0) |
| **Puente H L298N** | Sentido de giro (`IN3`) | `GPIO 27` | Salida digital (`OUTPUT`) |
| **Puente H L298N** | Sentido de giro (`IN4`) | `GPIO 26` | Salida digital (`OUTPUT`) |
| **Display OLED SH1106** | $I^2C$ SDA | `GPIO 21` | Línea de datos OLED ($128\times 64$, dirección `0x3C`) |
| **Display OLED SH1106** | $I^2C$ SCL | `GPIO 22` | Línea de reloj OLED ($128\times 64$) |

> ⚙️ **Calibración Experimental del Encoder:**  
> $$N_{\text{rev}} = 960\ \text{ticks/revolución}$$

---

## 3. Fórmulas de Conversión

La velocidad angular se estima periódicamente con $T_s = 0.1\,\text{s}$ ($f_s = 10\,\text{Hz}$):

### 3.1. Velocidad Angular en Radianes por Segundo ($\text{rad/s}$)
$$\omega[k] = \frac{2\pi \cdot \Delta N[k]}{N_{\text{rev}} \cdot \Delta t} \quad [\text{rad/s}]$$

### 3.2. Velocidad Angular en Revoluciones por Minuto ($\text{rpm}$)
$$n[k] = \frac{60 \cdot \Delta N[k]}{N_{\text{rev}} \cdot \Delta t} \quad [\text{rpm}]$$

donde:
* $\Delta N[k] = N[k] - N[k-1]$: incremento de ticks contados en el intervalo.
* $\Delta t = t[k] - t[k-1] \approx 0.1\text{ s}$: periodo de muestreo efectivo.
* $N_{\text{rev}} = 960$: número de cuentas por una revolución completa del eje de salida.

---

## 4. Implementación y Código en el Repositorio

### 4.1. Firmware del ESP32 (PlatformIO / Arduino C++)
Ubicación del código: [`firmware/esp32_motor_step/src/main.cpp`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step/src/main.cpp)  
Archivo de configuración: [`firmware/esp32_motor_step/platformio.ini`](file:///home/d3im3r/ros2-for-control-dc-motor-system/firmware/esp32_motor_step/platformio.ini)

Fragmento clave de la interrupción del encoder y cálculo de velocidad:
```cpp
// Interrupción de hardware para el encoder
void IRAM_ATTR encoderISR() {
  bool A = digitalRead(ENCA);
  bool B = digitalRead(ENCB);

  if (A != B)
    encoder_count--;
  else
    encoder_count++;
}

// Callback periódico del timer micro-ROS (Ts = 100 ms)
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  unsigned long current_time_ms = millis();
  float dt = (current_time_ms - previous_time_ms) * 0.001f;
  previous_time_ms = current_time_ms;

  noInterrupts();
  int32_t current_count = encoder_count;
  interrupts();

  int32_t delta_count = current_count - previous_count;
  previous_count = current_count;

  velocity_rad_s = (2.0f * PI * (float)delta_count) / (COUNTS_PER_REV * dt);
  velocity_rpm = (60.0f * (float)delta_count) / (COUNTS_PER_REV * dt);

  vel_rad_s_msg.data = velocity_rad_s;
  vel_rpm_msg.data = velocity_rpm;

  rcl_publish(&pub_vel_rad_s, &vel_rad_s_msg, NULL);
  rcl_publish(&pub_vel_rpm, &vel_rpm_msg, NULL);
}
```

### 4.2. Launch de Validación en ROS 2
Ubicación del launch: [`ros2_ws/src/dc_motor_bringup/launch/stage_01_instrumentation.launch.py`](file:///home/d3im3r/ros2-for-control-dc-motor-system/ros2_ws/src/dc_motor_bringup/launch/stage_01_instrumentation.launch.py)

```bash
# Lanzar la instrumentación y monitor de visualización
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```

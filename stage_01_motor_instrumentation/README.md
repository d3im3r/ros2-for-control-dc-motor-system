# Stage 01: Motor Instrumentation

## 🎯 Guiding Question
> **Can I apply a known actuation to the motor and measure its dynamic response accurately?**

---

## 📌 Objectives
1. Experimentally calibrate the encoder counts per revolution ($N_{rev} = 960\text{ ticks/rev}$).
2. Implement the `motor_step_node` on the ESP32 using micro-ROS.
3. Configure PWM modulation using the ESP32 LEDC peripheral at $500\text{ Hz}$ with 8-bit resolution.
4. Periodically sample at $10\text{ Hz}$ ($T_s = 0.1\text{ s}$) and publish signed angular velocity in `rad/s` and `rpm`.
5. Display telemetry locally in real time on the SH1106 OLED screen.
6. Validate bidirectional communication and command execution from ROS 2.

---

## 🧪 Execution
To validate the instrumentation from ROS 2:
```bash
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```

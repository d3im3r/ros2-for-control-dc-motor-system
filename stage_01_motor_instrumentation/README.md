# Stage 01: Motor Instrumentation

## 🎯 Pregunta Orientadora
> **¿Puedo aplicar una acción conocida al motor y medir correctamente su respuesta?**

---

## 📌 Objetivos
1. Calibrar experimentalmente las cuentas por revolución del encoder ($N_{rev} = 960\text{ ticks/rev}$).
2. Implementar el nodo `motor_step_node` sobre el ESP32 con micro-ROS.
3. Configurar la modulación PWM mediante el periférico LEDC a $500\text{ Hz}$ y 8 bits de resolución.
4. Muestrear periódicamente a $10\text{ Hz}$ ($T_s = 0.1\text{ s}$) y publicar velocidad angular con signo en `rad/s` y `rpm`.
5. Visualizar localmente los datos en la pantalla OLED SH1106.
6. Validar la recepción de comandos y la publicación de tópicos desde ROS 2.

---

## 🧪 Ejecución
Para validar la instrumentación desde ROS 2:
```bash
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```

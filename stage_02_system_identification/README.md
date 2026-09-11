# Stage 02: System Identification

## 🎯 Pregunta Orientadora
> **¿Qué modelo representa adecuadamente la dinámica entrada-salida del motor?**

---

## 📌 Objetivos
1. Ejecutar pruebas escalón en lazo abierto a diferentes amplitudes de PWM ($30\%$, $45\%$, $60\%$).
2. Registrar la curva de reacción temporal $(\omega(t) \text{ vs. } t)$ en archivos CSV de 350 a 400 muestras a $10\text{ Hz}$.
3. Estimar la ganancia estática $K$, la constante de tiempo dominante $\tau$ y el tiempo de retardo aparente $\theta$.
4. Construir y comparar modelos FOP ($G_{FOP}(s) = \frac{K}{\tau s + 1}$) y FOPDT ($G_{FOPDT}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$).
5. Analizar la linealidad del sistema entre los diferentes puntos de operación.

---

## 🚀 Ejecución de Pruebas
Para lanzar la adquisición automatizada con un escalón del $45\%$:
```bash
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0
```

## 📊 Scripts de Análisis Offline
```bash
python3 stage_02_system_identification/analysis/identify_fop.py
python3 stage_02_system_identification/analysis/identify_fopdt.py
python3 stage_02_system_identification/analysis/compare_operating_points.py
```

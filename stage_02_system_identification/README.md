# Stage 02: System Identification

## 🎯 Guiding Question
> **What mathematical model accurately represents the input-output dynamics of the motor?**

---

## 📌 Objectives
1. Execute open-loop step response tests at different PWM amplitudes ($30\%$, $45\%$, $60\%$).
2. Record temporal reaction curves $(\omega(t) \text{ vs. } t)$ in CSV datasets of 350 to 400 samples at $10\text{ Hz}$.
3. Estimate static gain $K$, dominant time constant $\tau$, and apparent delay $\theta$.
4. Construct and compare FOP ($G_{\mathrm{FOP}}(s) = \frac{K}{\tau s + 1}$) and FOPDT ($G_{\mathrm{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$) models.
5. Analyze system linearity across different operating points.

---

## 🚀 Running Experiments
To launch automated acquisition with a $45\%$ PWM step:
```bash
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0
```

## 📊 Offline Analysis Scripts
```bash
python3 stage_02_system_identification/analysis/identify_fop.py
python3 stage_02_system_identification/analysis/identify_fopdt.py
python3 stage_02_system_identification/analysis/compare_operating_points.py
```

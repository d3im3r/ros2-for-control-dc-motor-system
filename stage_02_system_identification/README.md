# Stage 02: System Identification

<div align="center">

<img src="https://img.shields.io/badge/Stage-02-blue?style=for-the-badge" alt="Stage 02">
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" alt="Completed">
<img src="https://img.shields.io/badge/Focus-System_Identification_%26_Modeling-purple?style=for-the-badge" alt="System Identification">

</div>

---

## 🎯 Guiding Question
> **What mathematical model accurately represents the input-output dynamics of the motor?**

---

## 📌 Objectives

1. **Open-Loop Step Experiments:** Apply controlled step inputs at multiple operating points ($30\%$, $45\%$, and $60\%$ PWM) to characterize system behavior across different dynamic regimes.
2. **Synchronized Dataset Acquisition:** Record temporal reaction curves ($\omega(t) \text{ vs. } t$) at $10\text{ Hz}$ across standardized 40-second test profiles (400 samples/dataset).
3. **Parameter Estimation:** Estimate the static gain $K$, dominant time constant $\tau$, and apparent dead time $\theta$ using both graphical tangent/two-point methods and non-linear least squares optimization.
4. **Transfer Function Synthesis:** Construct First-Order (FOP) and First-Order Plus Dead Time (FOPDT) models in continuous Laplace domain:
   $$G_{\mathrm{FOP}}(s) = \frac{K}{\tau s + 1}, \qquad G_{\mathrm{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$$
5. **Linearity and Operating Point Analysis:** Assess gain variation and saturation limits across the operating range.

---

## ⏱️ Step Experiment Profile

Each automated identification trial runs a 40-second synchronized sequence:

```text
  PWM Input [%]
       ^
  U_0  |         +-------------------------+
       |         |                         |
       |         |                         |
    0  +---------+                         +---------> Time [s]
       0         5                        30        40
       <Baseline><------ Step Active ----->< Rest >
```

* **$t \in [0, 5)\text{ s}$:** Baseline rest period ($u(t) = 0\%$, $\omega(t) \approx 0\text{ rad/s}$).
* **$t \in [5, 30)\text{ s}$:** Step actuation applied ($u(t) = U_0 \in \{30\%, 45\%, 60\%\}$).
* **$t \in [30, 40]\text{ s}$:** Motor de-energized ($u(t) = 0\%$) to record deceleration and settle.

---

## 🧮 Mathematical Formulations & Parameter Extraction

### 1. Static Gain ($K$)
$$K = \frac{\Delta \omega_{\mathrm{ss}}}{\Delta u} = \frac{\omega_{\mathrm{ss}} - \omega_0}{u_{\mathrm{step}} - u_0} \quad \left[\frac{\text{rad/s}}{\%}\right]$$

### 2. Time Constant ($\tau$) & Dead Time ($\theta$) Methods

* **$63.2\%$ Classic Method:**
  $$\omega(t_{63.2\%}) = \omega_0 + 0.632 \cdot (\omega_{\mathrm{ss}} - \omega_0) \implies \tau \approx t_{63.2\%} - t_{\mathrm{step}}$$

* **Two-Point Method (Smith / Miller):**
  $$\omega(t_{28.3\%}) = \omega_0 + 0.283 \cdot (\omega_{\mathrm{ss}} - \omega_0)$$
  $$\omega(t_{63.2\%}) = \omega_0 + 0.632 \cdot (\omega_{\mathrm{ss}} - \omega_0)$$
  $$\tau = 1.5 \cdot (t_{63.2\%} - t_{28.3\%}), \qquad \theta = (t_{63.2\%} - t_{\mathrm{step}}) - \tau$$

* **Analytical Step Responses:**
  * **FOP Model:**
    $$\omega_{\mathrm{FOP}}(t) = \omega_0 + K \cdot \Delta u \cdot \left(1 - e^{-(t - t_0)/\tau}\right) \cdot u_s(t - t_0)$$
  * **FOPDT Model:**
    $$\omega_{\mathrm{FOPDT}}(t) = \omega_0 + K \cdot \Delta u \cdot \left(1 - e^{-(t - t_0 - \theta)/\tau}\right) \cdot u_s(t - t_0 - \theta)$$

---

## 🚀 Running Identification Experiments

### Automated Acquisition via ROS 2 Launch
To launch the automated experiment runner, data logger, and monitor for a specified PWM step:

```bash
# Step at 30% PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=30.0

# Step at 45% PWM (Nominal Operating Point)
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0

# Step at 60% PWM
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=60.0
```

Raw CSV datasets are automatically saved to `stage_02_system_identification/data/raw/pwm_<step>/`.

---

## 📊 Offline Analysis & Model Fitting

Execute the provided Python identification scripts to process experimental CSV data, fit models, and compute error metrics ($R^2$, $\text{RMSE}$):

```bash
# Fit First-Order Model (FOP)
python3 stage_02_system_identification/analysis/identify_fop.py

# Fit First-Order Plus Dead Time Model (FOPDT)
python3 stage_02_system_identification/analysis/identify_fopdt.py

# Compare models across 30%, 45%, and 60% PWM operating points
python3 stage_02_system_identification/analysis/compare_operating_points.py
```

---

## 📁 Directory Organization

```text
stage_02_system_identification/
├── README.md                            # Stage 02 presentation and identification workflow
├── analysis/                            # Offline Python model extraction scripts
│   ├── identify_fop.py
│   ├── identify_fopdt.py
│   └── compare_operating_points.py
├── data/                                # Experimental step response data
│   ├── raw/                             # Raw CSV acquisitions (pwm_30, pwm_45, pwm_60)
│   └── processed/                       # Filtered and normalized datasets
├── models/                              # Identified transfer function parameters (JSON / YAML)
│   └── README.md
├── plots/                               # Step response and model comparison figures
│   └── README.md
└── results/                             # Goodness-of-fit metrics and identification reports
    └── README.md
```

---

## 📖 Associated Academic Guide

For comprehensive derivations, nonlinear least squares fitting theory, and step-by-step mathematical proofs:
* **[Guide 2: System Identification of a DC Motor](../docs/guides/Inteligente_guia2.md)**

---

## ⏭️ Next Step

Proceed to **[Stage 03: Model Validation](../stage_03_model_validation/README.md)** to cross-validate identified transfer functions against unseen multi-step and PRBS excitation profiles.

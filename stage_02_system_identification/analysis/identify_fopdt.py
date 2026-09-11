#!/usr/bin/env python3
"""Estimación de modelo con retardo (FOPDT): G(s) = K*exp(-theta*s) / (tau*s + 1)"""

import sys
import numpy as np
import matplotlib.pyplot as plt


def identify_fopdt(csv_path):
    print(f"Cargando datos desde: {csv_path}")
    data = np.genfromtxt(csv_path, delimiter=',', skip_header=1)
    t = data[:, 0]
    vel = data[:, 1]
    pwm = data[:, 2]

    # Identificar salto de PWM
    pwm_initial = pwm[0]
    idx_step = np.where(np.abs(np.diff(pwm)) > 1.0)[0]
    if len(idx_step) > 0:
        idx_t0 = idx_step[0] + 1
        t0 = t[idx_t0]
        pwm_step = pwm[idx_t0]
    else:
        idx_t0 = 0
        t0 = t[0]
        pwm_step = pwm[-1]

    delta_u = pwm_step - pwm_initial

    # Estimar régimen permanente
    idx_settled = int(len(vel) * 0.7)
    idx_end = int(len(vel) * 0.9)
    omega_ss = np.mean(vel[idx_settled:idx_end])
    omega_0 = np.mean(vel[:max(1, idx_t0)])
    delta_omega = omega_ss - omega_0

    K = delta_omega / delta_u if delta_u != 0 else 0.0

    # Detección de inicio de movimiento (theta)
    noise_thresh = omega_0 + 0.02 * delta_omega
    idx_motion = np.where(vel[idx_t0:] > noise_thresh)[0]
    if len(idx_motion) > 0:
        t_inicio = t[idx_t0 + idx_motion[0]]
        theta = max(0.0, t_inicio - t0)
    else:
        t_inicio = t0
        theta = 0.0

    # Criterio del 63.2%
    target_vel = omega_0 + 0.632 * delta_omega
    idx_63 = np.where(vel[idx_t0:] >= target_vel)[0]
    if len(idx_63) > 0:
        t_63 = t[idx_t0 + idx_63[0]]
        tau = max(0.01, t_63 - t0 - theta)
    else:
        tau = 0.1

    print("========================================")
    print(f"Resultados FOPDT:")
    print(f"  K     = {K:.4f} rad/s / %PWM")
    print(f"  tau   = {tau:.4f} s")
    print(f"  theta = {theta:.4f} s")
    print(f"  t0    = {t0:.2f} s")
    print(f"  wss   = {omega_ss:.2f} rad/s")
    print("========================================")

    # Simulación FOPDT
    t_sim = t[idx_t0:idx_end]
    vel_fopdt = np.where(
        t_sim < (t0 + theta),
        omega_0,
        omega_0 + K * delta_u * (1.0 - np.exp(-(t_sim - t0 - theta) / tau))
    )

    plt.figure(figsize=(9, 5))
    plt.plot(t, vel, 'b-', label='Datos experimentales')
    plt.plot(t_sim, vel_fopdt, 'g--', label=f'Modelo FOPDT (K={K:.3f}, tau={tau:.3f}s, theta={theta:.3f}s)')
    plt.axvline(t0, color='gray', linestyle=':', label='Instante escalón t0')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.title(f'Identificación FOPDT - Escalón {delta_u:.1f}% PWM')
    plt.grid(True)
    plt.legend()
    plt.show()

    return K, tau, theta


if __name__ == '__main__':
    if len(sys.argv) > 1:
        identify_fopdt(sys.argv[1])
    else:
        print("Uso: python3 identify_fopdt.py <ruta_archivo.csv>")

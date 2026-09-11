#!/usr/bin/env python3
"""Comparación de parámetros dinámicos entre puntos de operación (30%, 45%, 60% PWM)."""

import sys
import numpy as np
import matplotlib.pyplot as plt
from identify_fop import identify_fop


def compare_points(files):
    results = []
    for f in files:
        print(f"\n--- Procesando {f} ---")
        try:
            k, tau = identify_fop(f)
            results.append((f, k, tau))
        except Exception as e:
            print(f"Error procesando {f}: {e}")

    print("\n==========================================")
    print("RESUMEN DE PUNTOS DE OPERACIÓN")
    print(f"{'Archivo':<30} | {'K (rad/s/%)':<12} | {'tau (s)':<10}")
    print("------------------------------------------")
    for fname, k, tau in results:
        print(f"{fname:<30} | {k:<12.4f} | {tau:<10.4f}")
    print("==========================================")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        compare_points(sys.argv[1:])
    else:
        print("Uso: python3 compare_operating_points.py <csv_30.csv> <csv_45.csv> <csv_60.csv>")

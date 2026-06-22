# -*- coding: utf-8 -*-
"""
=====================================================
  MARUCHAN COOLING — Ley del Enfriamiento de Newton
  Backend Flask — app.py
  Autor: Ingeniero Full-Stack + Experto en EDO
=====================================================

  Modelo matemático implementado:
    dT/dt = -k(T - Tm)

  Solución analítica (ecuación separable):
    T(t) = Tm + (T0 - Tm) * e^(-k*t)

  Donde:
    T(t) = temperatura en el tiempo t [°C]
    T0   = temperatura inicial [°C]
    Tm   = temperatura ambiente (medio) [°C]
    k    = constante de enfriamiento [min⁻¹] (positiva)
    t    = tiempo [minutos]
=====================================================
"""

import math
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# ── Inicialización de la app Flask ──────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Permite peticiones cross-origin para el frontend JS


# ── Ruta principal: sirve el HTML ────────────────────────────────────────────
@app.route('/')
def index():
    """Página principal de la aplicación."""
    return render_template('index.html')


# ── API: Cálculo de la curva de enfriamiento ─────────────────────────────────
@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    Endpoint POST que recibe parámetros y devuelve:
      - time_points  : lista de tiempos [0, 0.5, 1.0, ... , max_t]
      - temp_points  : lista de temperaturas T(t) correspondientes
      - t_ideal_exact: tiempo exacto (minutos) en que T = t_ideal
      - meta         : parámetros usados y ecuación formateada
    """
    data = request.get_json(silent=True) or {}

    # ── Validación y extracción de parámetros ────────────────────────────────
    try:
        T0      = float(data.get('t0',      100.0))   # Temperatura inicial [°C]
        Tm      = float(data.get('tm',       25.0))   # Temperatura ambiente [°C]
        k       = float(data.get('k',        0.04))   # Constante de enfriamiento (positiva)
        T_ideal = float(data.get('t_ideal',  55.0))   # Temperatura perfecta para comer [°C]
        max_t   = float(data.get('max_t',    90.0))   # Duración de la simulación [min]
    except (ValueError, TypeError):
        return jsonify({'error': 'Parámetros inválidos. Usa valores numéricos.'}), 400

    # ── Validaciones físicas ─────────────────────────────────────────────────
    if k <= 0:
        return jsonify({'error': 'La constante k debe ser mayor que cero.'}), 400
    if T0 <= Tm:
        return jsonify({'error': 'T0 debe ser mayor que la temperatura ambiente Tm.'}), 400
    if T_ideal <= Tm or T_ideal >= T0:
        return jsonify({'error': f'T_ideal ({T_ideal}°C) debe estar entre Tm ({Tm}°C) y T0 ({T0}°C).'}), 400

    # ── Cálculo analítico del tiempo ideal ───────────────────────────────────
    # Despejando t de T(t) = Tm + (T0 - Tm)*e^(-kt):
    #   t_ideal = (1/k) * ln((T0 - Tm) / (T_ideal - Tm))
    t_ideal_exact = (1.0 / k) * math.log((T0 - Tm) / (T_ideal - Tm))

    # ── Generación de la curva de enfriamiento ───────────────────────────────
    # Paso de 0.5 minutos para resolución suave
    step      = 0.25
    n_points  = int(max_t / step) + 1
    time_points = []
    temp_points = []

    for i in range(n_points):
        t    = i * step
        T_t  = Tm + (T0 - Tm) * math.exp(-k * t)   # Solución analítica
        time_points.append(round(t, 4))
        temp_points.append(round(T_t, 4))

    # ── Cálculo de estadísticas adicionales ──────────────────────────────────
    # Tiempo en que la sopa baja a temperatura ambiente + 5°C (casi fría, ¡ya es tarde!)
    t_too_cold = (1.0 / k) * math.log((T0 - Tm) / 5.0) if (T0 - Tm) > 5 else None

    # Temperatura en distintos hitos clave
    milestones = {
        '5min':  round(Tm + (T0 - Tm) * math.exp(-k * 5.0),  2),
        '10min': round(Tm + (T0 - Tm) * math.exp(-k * 10.0), 2),
        '15min': round(Tm + (T0 - Tm) * math.exp(-k * 15.0), 2),
        '30min': round(Tm + (T0 - Tm) * math.exp(-k * 30.0), 2),
    }

    # ── Respuesta JSON ────────────────────────────────────────────────────────
    return jsonify({
        'time_points':    time_points,
        'temp_points':    temp_points,
        't_ideal_exact':  round(t_ideal_exact, 2),
        't_too_cold':     round(t_too_cold, 2) if t_too_cold else None,
        'milestones':     milestones,
        'params': {
            'T0':      T0,
            'Tm':      Tm,
            'k':       k,
            'T_ideal': T_ideal,
            'max_t':   max_t,
        },
        # Ecuación formateada para mostrar en frontend
        'equation': f'T(t) = {Tm} + ({T0} - {Tm}) · e^(−{k}·t)',
    })


# ── API: Información del modelo matemático ────────────────────────────────────
@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Devuelve la descripción del modelo matemático en JSON."""
    return jsonify({
        'edo':      'dT/dt = -k(T - Tm)',
        'solucion': 'T(t) = Tm + (T0 - Tm) * e^(-k*t)',
        'pasos_derivacion': [
            'Separación de variables: dT/(T - Tm) = -k dt',
            'Integración ambos lados: ln|T - Tm| = -kt + C',
            'Exponenciar: T - Tm = A·e^(-kt)',
            'Condición inicial T(0) = T0: A = T0 - Tm',
            'Solución final: T(t) = Tm + (T0 - Tm)·e^(-kt)',
        ],
        'variables': {
            'T(t)': 'Temperatura en tiempo t [°C]',
            'T0':   'Temperatura inicial [°C]',
            'Tm':   'Temperatura del medio ambiente [°C]',
            'k':    'Constante de enfriamiento [min⁻¹] > 0',
            't':    'Tiempo [minutos]',
        }
    })


# ── Punto de entrada ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("\n" + "="*55)
    print("  [*] MARUCHAN COOLING -- Servidor iniciado")
    print("  [=] Ley del Enfriamiento de Newton")
    print("  [>] http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')

# 🍜 Maruchan Cooling — Ley del Enfriamiento de Newton

> *Una aplicación web interactiva que enseña ecuaciones diferenciales a través de la historia épica de un estudiante de ingeniería hambriento a las 2 AM.*

---

## 📖 La Historia

Son las **2:47 AM**. Aarón lleva 6 horas frente al compilador. El estómago ruge.
La solución: una Maruchan instantánea. El problema: está **hirviendo a 100°C**.

Comerla ahora → quemadura garantizada.
Esperarla demasiado → sopa fría, amargura infinita.

**¿Cuántos minutos exactos debe esperar?** La respuesta está en una EDO separable de primer orden.

---

## 🧮 El Modelo Matemático

### La EDO — Ley de Newton (1701)

$$\frac{dT}{dt} = -k\,(T - T_m)$$

### Solución por separación de variables

| Paso | Operación | Resultado |
|------|-----------|-----------|
| 1 | Separar variables | $\dfrac{dT}{T - T_m} = -k\,dt$ |
| 2 | Integrar ambos lados | $\ln\|T - T_m\| = -kt + C$ |
| 3 | Exponenciar | $T - T_m = A\,e^{-kt}$ |
| 4 | Condición inicial $T(0)=T_0$ | $A = T_0 - T_m$ |
| 5 | **Solución final** | $T(t) = T_m + (T_0 - T_m)\,e^{-kt}$ |

### Tiempo óptimo para comer

$$t^* = \frac{1}{k}\,\ln\!\left(\frac{T_0 - T_m}{T^* - T_m}\right)$$

Con $T_0=100°C$, $T_m=25°C$, $T^*=55°C$, $k=0.04\,\text{min}^{-1}$:

$$t^* \approx 22.91 \text{ minutos}$$

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.9+
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/maruchan-cooling.git
cd maruchan-cooling
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
python app.py
```

### 5. Abrir en el navegador

```
http://127.0.0.1:5000
```

---

## 🏗️ Estructura del Proyecto

```
maruchan-cooling/
│
├── app.py                  # Backend Flask — API REST
│
├── templates/
│   └── index.html          # Frontend — HTML + MathJax + Chart.js
│
├── static/
│   ├── css/
│   │   └── style.css       # Diseño dark mode neon-noir
│   ├── js/
│   │   └── main.js         # Lógica interactiva + Chart.js
│   └── images/
│       ├── student_hero.png    # Ilustración IA — el estudiante
│       └── maruchan_art.png    # Ilustración IA — la sopa
│
├── requirements.txt        # Dependencias Python
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🔌 API Endpoint

### `POST /api/calculate`

Calcula la curva de enfriamiento y el tiempo ideal.

**Request body (JSON):**

```json
{
  "t0":      100,   // Temperatura inicial [°C]
  "tm":       25,   // Temperatura ambiente [°C]
  "k":       0.04,  // Constante de enfriamiento [min⁻¹]
  "t_ideal":  55,   // Temperatura ideal para comer [°C]
  "max_t":    90    // Duración de la simulación [min]
}
```

**Response (JSON):**

```json
{
  "time_points":   [0, 0.25, 0.5, ...],
  "temp_points":   [100.0, 99.0, 98.0, ...],
  "t_ideal_exact": 22.91,
  "milestones": {
    "5min":  86.4,
    "10min": 75.27,
    "15min": 65.97,
    "30min": 45.24
  },
  "params": { "T0": 100, "Tm": 25, "k": 0.04, "T_ideal": 55 },
  "equation": "T(t) = 25 + (100 - 25) · e^(−0.04·t)"
}
```

---

## 🎨 Tech Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python 3 + Flask |
| Frontend | HTML5 + Vanilla CSS + Vanilla JS |
| Matemáticas | MathJax 3 (LaTeX en el browser) |
| Gráficas | Chart.js 4 |
| Diseño | Dark mode neon-noir (CSS custom properties) |
| Fuentes | Inter + JetBrains Mono (Google Fonts) |

---

## 📐 Variables del Sistema

| Símbolo | Nombre | Unidad |
|---------|--------|--------|
| $T(t)$ | Temperatura en tiempo $t$ | °C |
| $T_0$ | Temperatura inicial | °C |
| $T_m$ | Temperatura del medio (ambiente) | °C |
| $k$ | Constante de enfriamiento | min⁻¹ |
| $t$ | Tiempo | minutos |
| $t^*$ | Tiempo ideal para comer | minutos |

---

## 📚 Contexto Académico

Este proyecto demuestra una aplicación real de las **Ecuaciones Diferenciales Ordinarias (EDO)**
en un contexto cotidiano, cubriendo:

- Modelado matemático de fenómenos físicos
- Resolución de EDOs separables de primer orden
- Aplicación de condiciones iniciales
- Visualización de soluciones analíticas

**Área:** Cálculo III / Ecuaciones Diferenciales — Ingeniería en Sistemas / Computación

---

## 📄 Licencia

MIT License — ver [LICENSE](LICENSE) para detalles.

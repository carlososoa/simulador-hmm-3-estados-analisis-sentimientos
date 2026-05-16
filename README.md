# Simulador HMM de 3 Estados — Análisis de Sentimientos

Simulador de Modelo Oculto de Markov (HMM) para analizar sentimientos en redes sociales. Genera secuencias sintéticas de tweets en español a partir de 3 estados ocultos: Positivo, Neutral y Negativo.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Arquitectura (MVC)

- **`model/hmm.py`** — Clase `HMM` con matrices de transición (A), emisión (B) y distribución inicial (π). Método `generate_sequence()` que retorna un `SimulationResult`.
- **`view/`** — 9 pantallas Pygame (`TitleScreen`, `ConfigScreen`, `SimulationScreen`, `SummaryScreen`, `TrendScreen`, `StationaryScreen`, `ConvergenceScreen`, `BarChartScreen`, `ConfusionScreen`).
- **`controller/game.py`** — `GameController` con el bucle principal, pila de pantallas y la instancia del HMM.

## Parámetros del modelo

### Matriz de transición A

|            | Positivo | Neutral | Negativo |
|------------|:--------:|:-------:|:--------:|
| Positivo   | 0.6      | 0.3     | 0.1      |
| Neutral    | 0.2      | 0.6     | 0.2      |
| Negativo   | 0.1      | 0.3     | 0.6      |

### Matriz de emisión B

|            | v-pos | v-neu | v-neg |
|------------|:-----:|:-----:|:-----:|
| Positivo   | 0.7   | 0.2   | 0.1   |
| Neutral    | 0.2   | 0.6   | 0.2   |
| Negativo   | 0.1   | 0.2   | 0.7   |

### Distribución inicial π

Positivo: 0.2 · Neutral: 0.6 · Negativo: 0.2

## Análisis y resultados

La carpeta `análisis/` contiene scripts y resultados de una simulación de 1000 iteraciones del modelo:

- **`simulacion.py`** — Ejecuta la simulación y genera automáticamente todos los gráficos
- **`heatmap_transicion.py`** — Genera mapa de calor comparativo de la matriz A teórica vs empírica
- **`simulacion_resultados.csv`** — Secuencia completa de 1000 tuits generados
- **`metricas.txt`** — Métricas detalladas: matrices empíricas, conteos, distribuciones
- **`*.png`** — 7 gráficos: distribución, evolución temporal, convergencia, matriz de confusión, etc.

Para reproducir los resultados:
```bash
python análisis/simulacion.py
```

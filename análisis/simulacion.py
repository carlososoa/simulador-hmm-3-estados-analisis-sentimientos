import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv

from model.hmm import HMM, STATE_NAMES, STATE_COLORS, OBS_NAMES
from words import generate_tweet

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def save_pie_chart(distribution, counts):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    labels = [f"{STATE_NAMES[i]} ({counts[i]})" for i in range(3)]
    wedges, texts, autotexts = ax.pie(
        distribution, labels=labels, colors=colors_norm, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 11, 'color': 'white'}
    )
    for t in autotexts:
        t.set_color('white')
        t.set_fontweight('bold')
        t.set_fontsize(12)
    for t in texts:
        t.set_fontsize(11)
    ax.set_title('Distribucion de Sentimientos', fontsize=14, fontweight='bold', pad=20, color='white')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'pie_chart.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)

def save_step_chart(states):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    x = np.arange(len(states))
    for i in range(len(states) - 1):
        ax.plot([x[i], x[i + 1]], [states[i], states[i + 1]],
                color=colors_norm[states[i]], linewidth=2, alpha=0.8)
    ax.plot(x[-1], states[-1], 'o', color=colors_norm[states[-1]], markersize=6)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(STATE_NAMES, color='white', fontsize=10)
    ax.set_xlabel('Numero de Tweet', fontsize=11, color='white')
    ax.set_ylabel('Sentimiento', fontsize=11, color='white')
    ax.set_title('Evolucion Temporal del Sentimiento', fontsize=14, fontweight='bold', pad=15, color='white')
    ax.set_ylim(-0.5, 2.5)
    ax.grid(True, alpha=0.2, color='gray')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines['bottom'].set_color('#3a4076')
    ax.spines['top'].set_color('#3a4076')
    ax.spines['left'].set_color('#3a4076')
    ax.spines['right'].set_color('#3a4076')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'step_chart.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)

def save_stationary_chart(vectors):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    x = np.arange(vectors.shape[0])
    for i in range(3):
        ax.plot(x, vectors[:, i], label=STATE_NAMES[i], color=colors_norm[i], linewidth=2)
    ax.set_title('Evolucion del Vector Estacionario', fontsize=14, fontweight='bold', pad=15, color='white')
    ax.set_xlabel('Iteracion (k)', fontsize=11, color='white')
    ax.set_ylabel('Probabilidad', fontsize=11, color='white')
    ax.legend(fontsize=10, facecolor='#2a3056', edgecolor='#3a4076', labelcolor='white')
    ax.grid(True, alpha=0.2, color='gray')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines['bottom'].set_color('#3a4076')
    ax.spines['top'].set_color('#3a4076')
    ax.spines['left'].set_color('#3a4076')
    ax.spines['right'].set_color('#3a4076')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'stationary_chart.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)

def save_convergence_chart(states, theoretical):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    n = len(states)
    counts = np.zeros((3, n), dtype=float)
    for k in range(n):
        if k == 0:
            counts[states[k], k] = 1.0
        else:
            counts[:, k] = counts[:, k - 1]
            counts[states[k], k] += 1.0
    cumulative = counts / np.arange(1, n + 1)
    x = np.arange(n)
    for i in range(3):
        ax.plot(x, cumulative[i], label=STATE_NAMES[i] + ' (empirica)',
                color=colors_norm[i], linewidth=1.5, alpha=0.85)
        ax.axhline(y=theoretical[i], color=colors_norm[i], linestyle='--',
                   linewidth=2, alpha=0.7,
                   label=STATE_NAMES[i] + f' (teorica: {theoretical[i]:.3f})')
    ax.set_title('Convergencia de Probabilidades Empiricas', fontsize=14, fontweight='bold', pad=15, color='white')
    ax.set_xlabel('Iteracion', fontsize=11, color='white')
    ax.set_ylabel('Probabilidad', fontsize=11, color='white')
    ax.legend(fontsize=9, facecolor='#2a3056', edgecolor='#3a4076', labelcolor='white')
    ax.grid(True, alpha=0.2, color='gray')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines['bottom'].set_color('#3a4076')
    ax.spines['top'].set_color('#3a4076')
    ax.spines['left'].set_color('#3a4076')
    ax.spines['right'].set_color('#3a4076')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'convergence_chart.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)

def save_sequence_chart(states, observations):
    state_colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    obs_colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in STATE_COLORS]
    n = min(len(states), 50)
    fig, ax = plt.subplots(figsize=(11, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    ax.tick_params(colors='white', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#3a4076')
    ax.set_xlim(-0.5, n - 0.5)
    ax.margins(x=0.01)
    x = np.arange(n)
    bottom_colors = [state_colors_norm[s] for s in states[:n]]
    top_colors = [obs_colors_norm[o] for o in observations[:n]]
    ax.bar(x, np.full(n, 0.5), bottom=np.zeros(n), width=1.0,
           color=bottom_colors, edgecolor='none', linewidth=0)
    ax.bar(x, np.full(n, 0.5), bottom=np.full(n, 0.5), width=1.0,
           color=top_colors, edgecolor='none', linewidth=0)
    ax.set_yticks([0.25, 0.75])
    ax.set_yticklabels(['Estado', 'Observacion'], fontsize=10, color='white')
    ax.set_ylim(0, 1)
    ax.set_xlabel('Numero de Tweet', fontsize=11, color='white')
    ax.set_title('Secuencia de Estados y Observaciones (primeros 50)', fontsize=14, fontweight='bold', pad=12, color='white')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'sequence_chart.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)

def save_confusion_matrix(states, observations):
    matrix = np.zeros((3, 3), dtype=int)
    for s, o in zip(states, observations):
        matrix[s, o] += 1
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    normed = matrix / row_sums
    cmap = plt.cm.Blues
    im = ax.imshow(normed, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Proporcion', color='white', fontsize=10)
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    colors_norm = [(76 / 255, 175 / 255, 80 / 255),
                   (255 / 255, 193 / 255, 7 / 255),
                   (244 / 255, 67 / 255, 54 / 255)]
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{int(matrix[i, j])}\n({normed[i, j]:.1%})",
                    ha='center', va='center', color='white', fontsize=10, fontweight='bold')
    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(OBS_NAMES, color='white', fontsize=9)
    ax.set_yticklabels(STATE_NAMES, color='white', fontsize=9)
    for tick, color in zip(ax.get_yticklabels(), colors_norm):
        tick.set_color(color)
    for tick, color in zip(ax.get_xticklabels(), colors_norm):
        tick.set_color(color)
    ax.set_title('Matriz de Confusion: Estados vs Observaciones', fontsize=14, fontweight='bold', pad=15, color='white')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix.png'), dpi=120, bbox_inches='tight',
                facecolor='#1a2036')
    plt.close(fig)
    return matrix

def main():
    print("Inicializando HMM...")
    hmm = HMM()

    print(f"\nMatriz de transicion A:")
    print(hmm.A)
    print(f"\nMatriz de emision B:")
    print(hmm.B)
    print(f"\nProbabilidades iniciales pi:")
    print(hmm.pi)

    theoretical = hmm.stationary_distribution()
    print(f"\nDistribucion estacionaria teorica (pi*):")
    for i, name in enumerate(STATE_NAMES):
        print(f"  {name}: {theoretical[i]:.4f}")

    N = 1000
    print(f"\nGenerando secuencia de {N} iteraciones...")
    result = hmm.generate_sequence(N, generate_tweet)

    states = np.array(result.states)
    observations = np.array(result.observations)
    vectors = np.array(result.vectors)
    tweets = result.tweets

    counts = [0, 0, 0]
    for s in states:
        counts[s] += 1
    distribution_pct = [c / N * 100 for c in counts]

    print(f"\n=== RESULTADOS ===")
    print(f"Total de tweets: {N}")
    for i in range(3):
        print(f"  {STATE_NAMES[i]}: {counts[i]} ({distribution_pct[i]:.1f}%)")

    transitions = {}
    for i in range(N - 1):
        key = (states[i], states[i + 1])
        transitions[key] = transitions.get(key, 0) + 1
    most_common = max(transitions, key=transitions.get) if transitions else (0, 0)
    print(f"\nTransicion mas comun: {STATE_NAMES[most_common[0]]} -> {STATE_NAMES[most_common[1]]} ({transitions[most_common]}/{N-1})")

    transition_matrix_emp = np.zeros((3, 3))
    for (s_from, s_to), cnt in transitions.items():
        transition_matrix_emp[s_from, s_to] = cnt
    row_sums = transition_matrix_emp.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    transition_matrix_emp_norm = transition_matrix_emp / row_sums
    print(f"\nMatriz de transicion empirica (normalizada):")
    print(np.round(transition_matrix_emp_norm, 3))

    empirical_dist = np.array(counts) / N
    print(f"\nDistribucion empirica de estados: {np.round(empirical_dist, 4)}")
    print(f"Distribucion estacionaria teorica: {np.round(theoretical, 4)}")

    print(f"\nGuardando graficos...")
    save_pie_chart(distribution_pct, counts)
    print("  pie_chart.png OK")
    save_step_chart(states)
    print("  step_chart.png OK")
    save_stationary_chart(vectors)
    print("  stationary_chart.png OK")
    save_convergence_chart(states, theoretical)
    print("  convergence_chart.png OK")
    save_sequence_chart(states, observations)
    print("  sequence_chart.png OK")
    conf_matrix = save_confusion_matrix(states, observations)
    print("  confusion_matrix.png OK")

    csv_path = os.path.join(OUTPUT_DIR, 'simulacion_resultados.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['iteracion', 'estado', 'observacion', 'tweet'])
        for i in range(N):
            writer.writerow([i + 1, STATE_NAMES[states[i]], OBS_NAMES[observations[i]], tweets[i]])
    print(f"  {csv_path} OK")

    metrics_path = os.path.join(OUTPUT_DIR, 'metricas.txt')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        f.write("=== METRICAS DE SIMULACION HMM ===\n")
        f.write(f"Iteraciones: {N}\n\n")
        f.write("--- Matriz de Transicion A (teorica) ---\n")
        f.write(str(hmm.A) + "\n\n")
        f.write("--- Matriz de Emision B (teorica) ---\n")
        f.write(str(hmm.B) + "\n\n")
        f.write("--- Probabilidades Iniciales pi ---\n")
        f.write(str(hmm.pi) + "\n\n")
        f.write("--- Distribucion Estacionaria Teorica ---\n")
        for i, name in enumerate(STATE_NAMES):
            f.write(f"  {name}: {theoretical[i]:.4f}\n")
        f.write(f"\n--- Conteo de Estados ---\n")
        for i in range(3):
            f.write(f"  {STATE_NAMES[i]}: {counts[i]} ({distribution_pct[i]:.1f}%)\n")
        f.write(f"\n--- Distribucion Empirica ---\n")
        f.write(f"  {np.round(empirical_dist, 4)}\n")
        f.write(f"\n--- Matriz de Transicion Empirica (conteos) ---\n")
        f.write(str(transition_matrix_emp.astype(int)) + "\n\n")
        f.write("--- Matriz de Transicion Empirica (normalizada) ---\n")
        f.write(str(np.round(transition_matrix_emp_norm, 3)) + "\n\n")
        f.write(f"--- Transicion mas comun ---\n")
        f.write(f"  {STATE_NAMES[most_common[0]]} -> {STATE_NAMES[most_common[1]]}: {transitions[most_common]} veces\n\n")
        f.write("--- Matriz de Confusion (conteos estado vs observacion) ---\n")
        f.write(str(conf_matrix) + "\n")
    print(f"  {metrics_path} OK")

    print(f"\nSimulacion completada exitosamente.")

if __name__ == '__main__':
    main()

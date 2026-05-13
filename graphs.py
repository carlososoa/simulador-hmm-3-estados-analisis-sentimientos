import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
import numpy as np


def fig_to_surface(fig, dpi=100):
    fig.set_dpi(dpi)
    fig.patch.set_facecolor('#1a2036')
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    return pygame.image.frombuffer(buf, canvas.get_width_height(), "RGBA")


def create_pie_chart(distribution, labels, colors, title):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in colors]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')

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

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='white')
    fig.tight_layout()
    return fig


def create_line_chart(data, labels, colors, title, xlabel, ylabel):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in colors]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')

    x = np.arange(data.shape[1])
    for i in range(data.shape[0]):
        ax.plot(x, data[i], label=labels[i], color=colors_norm[i], linewidth=2)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='white')
    ax.set_xlabel(xlabel, fontsize=11, color='white')
    ax.set_ylabel(ylabel, fontsize=11, color='white')
    ax.legend(fontsize=10, facecolor='#2a3056', edgecolor='#3a4076', labelcolor='white')
    ax.grid(True, alpha=0.2, color='gray')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines['bottom'].set_color('#3a4076')
    ax.spines['top'].set_color('#3a4076')
    ax.spines['left'].set_color('#3a4076')
    ax.spines['right'].set_color('#3a4076')
    fig.tight_layout()
    return fig


def create_step_chart(states, labels, colors, title, xlabel, ylabel):
    colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in colors]
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')

    x = np.arange(len(states))
    for i in range(len(states) - 1):
        ax.plot([x[i], x[i + 1]], [states[i], states[i + 1]],
                color=colors_norm[states[i]], linewidth=2, alpha=0.8)
    ax.plot(x[-1], states[-1], 'o', color=colors_norm[states[-1]], markersize=6)

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(labels, color='white', fontsize=10)
    ax.set_xlabel(xlabel, fontsize=11, color='white')
    ax.set_ylabel(ylabel, fontsize=11, color='white')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='white')
    ax.set_ylim(-0.5, 2.5)
    ax.grid(True, alpha=0.2, color='gray')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines['bottom'].set_color('#3a4076')
    ax.spines['top'].set_color('#3a4076')
    ax.spines['left'].set_color('#3a4076')
    ax.spines['right'].set_color('#3a4076')
    fig.tight_layout()
    return fig


def create_sequence_bar_charts(states, observations, state_labels, obs_labels,
                                state_colors, obs_colors, title):
    state_colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in state_colors]
    obs_colors_norm = [(r / 255, g / 255, b / 255) for r, g, b in obs_colors]
    n = len(states)

    fig, ax = plt.subplots(figsize=(11, 4.5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')
    ax.tick_params(colors='white', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#3a4076')
    ax.set_xlim(-0.5, n - 0.5)
    ax.margins(x=0.01)

    x = np.arange(n)

    bottom_colors = [state_colors_norm[s] for s in states]
    top_colors = [obs_colors_norm[o] for o in observations]

    ax.bar(x, np.full(n, 0.5), bottom=np.zeros(n), width=1.0,
           color=bottom_colors, edgecolor='none', linewidth=0)
    ax.bar(x, np.full(n, 0.5), bottom=np.full(n, 0.5), width=1.0,
           color=top_colors, edgecolor='none', linewidth=0)

    ax.set_yticks([0.25, 0.75])
    ax.set_yticklabels(['Estado', 'Observación'], fontsize=10, color='white')
    ax.set_ylim(0, 1)
    ax.set_xlabel('Número de Tweet', fontsize=11, color='white')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=12, color='white')

    fig.tight_layout()
    return fig


def create_confusion_matrix(matrix, row_labels, col_labels, title):
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('#1a2036')
    ax.set_facecolor('#1a2036')

    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    normed = matrix / row_sums

    cmap = plt.cm.Blues
    im = ax.imshow(normed, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Proporción', color='white', fontsize=10)
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')

    colors_norm = [(76 / 255, 175 / 255, 80 / 255),
                   (255 / 255, 193 / 255, 7 / 255),
                   (244 / 255, 67 / 255, 54 / 255)]

    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax.text(j, i, f"{int(matrix[i, j])}\n({normed[i, j]:.1%})",
                    ha='center', va='center', color='white', fontsize=10, fontweight='bold')

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, color='white', fontsize=9)
    ax.set_yticklabels(row_labels, color='white', fontsize=9)

    for tick, color in zip(ax.get_yticklabels(), colors_norm):
        tick.set_color(color)
    for tick, color in zip(ax.get_xticklabels(), colors_norm):
        tick.set_color(color)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='white')
    fig.tight_layout()
    return fig

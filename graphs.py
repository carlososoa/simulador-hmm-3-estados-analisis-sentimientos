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

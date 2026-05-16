import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = '/mnt/c/Users/AndresOsorio/Documents/markov/análisis'

A_teo = np.array([
    [0.6, 0.3, 0.1],
    [0.2, 0.6, 0.2],
    [0.1, 0.3, 0.6]
])

A_emp = np.array([
    [0.634, 0.272, 0.094],
    [0.202, 0.593, 0.205],
    [0.087, 0.308, 0.605]
])

labels = ['Positivo', 'Neutral', 'Negativo']

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
fig.patch.set_facecolor('#1a2036')

titles = ['Matriz A Teorica', 'Matriz A Empirica']
matrices = [A_teo, A_emp]

for idx, (ax, mat, title) in enumerate(zip(axes, matrices, titles)):
    ax.set_facecolor('#1a2036')
    im = ax.imshow(mat, cmap='YlOrRd', aspect='auto', vmin=0, vmax=0.7)

    for i in range(3):
        for j in range(3):
            val = mat[i, j]
            color = 'white' if val < 0.45 else 'black'
            ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                    color=color, fontsize=13, fontweight='bold')

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(labels, color='white', fontsize=10)
    ax.set_yticklabels(labels, color='white', fontsize=10)
    ax.tick_params(colors='white')

    ax.set_xlabel('Estado destino', fontsize=11, color='white')
    ax.set_ylabel('Estado origen', fontsize=11, color='white')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=12, color='white')

    if idx == 0:
        for tick, color in zip(ax.get_yticklabels(), [(76/255,175/255,80/255), (255/255,193/255,7/255), (244/255,67/255,54/255)]):
            tick.set_color(color)

cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('Probabilidad', color='white', fontsize=10)
cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')

fig.suptitle('Comparacion: Matriz de Transicion Teorica vs Empirica',
             fontsize=15, fontweight='bold', color='white', y=1.02)
fig.tight_layout(rect=[0, 0, 0.9, 1])
fig.savefig(f'{OUTPUT_DIR}/matriz_A_comparacion.png', dpi=150, bbox_inches='tight',
            facecolor='#1a2036')
plt.close(fig)
print("OK - matriz_A_comparacion.png generado")

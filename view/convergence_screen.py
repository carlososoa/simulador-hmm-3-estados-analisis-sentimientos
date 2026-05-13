import pygame
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, GRAY, WHITE
from view.components import Button
from model.hmm import STATE_NAMES, STATE_COLORS
from graphs import create_convergence_chart, fig_to_surface


class ConvergenceScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_info = pygame.font.Font(None, 22)
        self.font_btn = pygame.font.Font(None, 26)
        self.font_state = pygame.font.Font(None, 24)

        self.btn_back = Button(
            (80, 640, 180, 50),
            "Anterior", self.font_btn,
            (60, 60, 80), (80, 80, 110), callback=self.go_back
        )
        self.btn_next = Button(
            (1000, 640, 200, 50),
            "Siguiente", self.font_btn,
            ACCENT_COLOR, ACCENT_HOVER, callback=self.go_next
        )
        self.btn_restart = Button(
            (820, 640, 160, 50),
            "Reiniciar", self.font_btn,
            (180, 60, 60), (220, 80, 80), callback=self.go_restart
        )

        self.chart_surface = None
        self.theoretical = None

    def go_back(self):
        self.controller.switch_to(5)

    def go_next(self):
        self.controller.switch_to(7)

    def go_restart(self):
        self.controller.switch_to(0)

    def on_enter(self):
        result = self.controller.simulation_result
        hmm = self.controller.hmm
        if not result or result.n == 0:
            return

        self.theoretical = hmm.stationary_distribution()

        cached = self.controller.chart_cache.get("convergence")
        if cached:
            self.chart_surface = cached
            return

        n = result.n
        counts = np.zeros((3, n), dtype=float)
        for k in range(n):
            if k == 0:
                counts[result.states[k], k] = 1.0
            else:
                counts[:, k] = counts[:, k - 1]
                counts[result.states[k], k] += 1.0

        cumulative = counts / np.arange(1, n + 1)

        fig = create_convergence_chart(
            cumulative,
            self.theoretical,
            STATE_NAMES,
            STATE_COLORS,
            "Convergencia de Probabilidades Empíricas",
            "Iteración",
            "Probabilidad"
        )
        self.chart_surface = fig_to_surface(fig)
        plt.close(fig)

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Convergencia de Probabilidades Empíricas", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)
        draw_text(screen, "Frecuencia acumulada de cada estado vs distribución estacionaria teórica",
                  self.font_info, GRAY, 640, 65, center=True)

        if self.chart_surface:
            chart_rect = self.chart_surface.get_rect(center=(640, 360))
            screen.blit(self.chart_surface, chart_rect)

        if self.theoretical is not None:
            info_y = 600
            draw_text(screen, "Distribución estacionaria teórica (π*):",
                      self.font_info, WHITE, 640, info_y, center=True)
            for i, name in enumerate(STATE_NAMES):
                x = 350 + i * 280
                color = STATE_COLORS[i]
                pygame.draw.rect(screen, color, (x - 8, info_y + 30, 10, 10), border_radius=2)
                draw_text(screen, f"{name}: {self.theoretical[i]:.4f}",
                          self.font_state, color, x + 6, info_y + 26)

        self.btn_back.draw(screen)
        self.btn_next.draw(screen)
        self.btn_restart.draw(screen)

    def handle_event(self, event):
        self.btn_back.handle_event(event)
        self.btn_next.handle_event(event)
        self.btn_restart.handle_event(event)

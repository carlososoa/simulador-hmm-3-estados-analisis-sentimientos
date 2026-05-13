import pygame
import numpy as np
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, GRAY, WHITE
from view.components import Button
from model.hmm import STATE_NAMES, STATE_COLORS
from graphs import create_line_chart, fig_to_surface


class StationaryScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_info = pygame.font.Font(None, 22)
        self.font_btn = pygame.font.Font(None, 26)

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

        self.chart_surface = None
        self.final_vector = None

    def go_back(self):
        self.controller.switch_to(4)

    def go_next(self):
        self.controller.switch_to(6)

    def on_enter(self):
        result = self.controller.simulation_result
        if not result or result.n == 0:
            return

        vectors = np.array(result.vectors)

        cached = self.controller.chart_cache.get("stationary")
        if cached:
            self.chart_surface = cached
        else:
            fig = create_line_chart(
                vectors.T,
                STATE_NAMES,
                STATE_COLORS,
                "Evolución del Vector Estacionario",
                "Iteración (k)",
                "Probabilidad"
            )
            self.chart_surface = fig_to_surface(fig)
            import matplotlib.pyplot as plt
            plt.close(fig)

        self.final_vector = vectors[-1]

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Evolución del Vector Estacionario", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)
        draw_text(screen, "Teorema de Perron-Frobenius: convergencia a distribución estacionaria",
                  self.font_info, GRAY, 640, 65, center=True)

        if self.chart_surface:
            chart_rect = self.chart_surface.get_rect(center=(640, 370))
            screen.blit(self.chart_surface, chart_rect)

        if self.final_vector is not None:
            info_y = 600
            draw_text(screen, "Vector estacionario (distribución límite):",
                      self.font_info, WHITE, 640, info_y, center=True)
            vec_text = "  |  ".join(
                f"{STATE_NAMES[i]}: {self.final_vector[i]:.4f}"
                for i in range(3)
            )
            draw_text(screen, vec_text, self.font_info, GRAY, 640, info_y + 25, center=True)

        self.btn_back.draw(screen)
        self.btn_next.draw(screen)

    def handle_event(self, event):
        self.btn_back.handle_event(event)
        self.btn_next.handle_event(event)

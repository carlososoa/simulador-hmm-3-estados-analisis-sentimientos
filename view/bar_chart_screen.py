import pygame
import numpy as np
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, GRAY
from view.components import Button
from model.hmm import STATE_NAMES, STATE_COLORS, OBS_NAMES
from graphs import create_sequence_bar_charts, fig_to_surface


class BarChartScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_btn = pygame.font.Font(None, 26)

        self.btn_next = Button(
            (1000, 640, 200, 50),
            "Siguiente", self.font_btn,
            ACCENT_COLOR, ACCENT_HOVER, callback=self.go_next
        )
        self.btn_back = Button(
            (80, 640, 180, 50),
            "Anterior", self.font_btn,
            (60, 60, 80), (80, 80, 110), callback=self.go_back
        )

        self.chart_surface = None

    def go_next(self):
        self.controller.switch_to(8)

    def go_back(self):
        self.controller.switch_to(6)

    def on_enter(self):
        result = self.controller.simulation_result
        if not result or result.n == 0:
            return

        cached = self.controller.chart_cache.get("barchart")
        if cached:
            self.chart_surface = cached
            return

        states = np.array(result.states)
        observations = np.array(result.observations)

        fig = create_sequence_bar_charts(
            states, observations,
            STATE_NAMES, OBS_NAMES,
            STATE_COLORS, STATE_COLORS,
            "Secuencia de Estados y Observaciones"
        )
        self.chart_surface = fig_to_surface(fig)

        import matplotlib.pyplot as plt
        plt.close(fig)

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Secuencia de Estados y Observaciones", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)
        draw_text(screen, "Cada barra representa un tweet: abajo el estado oculto, arriba la observación",
                  pygame.font.Font(None, 22), GRAY, 640, 65, center=True)

        if self.chart_surface:
            chart_rect = self.chart_surface.get_rect(center=(640, 370))
            screen.blit(self.chart_surface, chart_rect)

        self.btn_back.draw(screen)
        self.btn_next.draw(screen)

    def handle_event(self, event):
        self.btn_back.handle_event(event)
        self.btn_next.handle_event(event)

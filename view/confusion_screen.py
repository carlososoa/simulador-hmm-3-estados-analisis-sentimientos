import pygame
import numpy as np
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, GRAY
from view.components import Button
from model.hmm import STATE_NAMES, OBS_NAMES
from graphs import create_confusion_matrix, fig_to_surface


class ConfusionScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_btn = pygame.font.Font(None, 26)

        self.btn_back = Button(
            (80, 640, 180, 50),
            "Anterior", self.font_btn,
            (60, 60, 80), (80, 80, 110), callback=self.go_back
        )
        self.btn_restart = Button(
            (1000, 640, 200, 50),
            "Reiniciar", self.font_btn,
            (180, 60, 60), (220, 80, 80), callback=self.go_restart
        )

        self.chart_surface = None

    def go_back(self):
        self.controller.switch_to(7)

    def go_restart(self):
        self.controller.switch_to(0)

    def on_enter(self):
        result = self.controller.simulation_result
        if not result or result.n == 0:
            return

        matrix = np.zeros((3, 3), dtype=int)
        for s, o in zip(result.states, result.observations):
            matrix[s, o] += 1

        fig = create_confusion_matrix(
            matrix,
            STATE_NAMES,
            OBS_NAMES,
            "Matriz de Confusión: Estados vs Observaciones"
        )
        self.chart_surface = fig_to_surface(fig)

        import matplotlib.pyplot as plt
        plt.close(fig)

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Matriz de Confusión", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)
        draw_text(screen, "Conteo de observaciones generadas por cada estado oculto",
                  pygame.font.Font(None, 22), GRAY, 640, 65, center=True)

        if self.chart_surface:
            chart_rect = self.chart_surface.get_rect(center=(640, 370))
            screen.blit(self.chart_surface, chart_rect)

        self.btn_back.draw(screen)
        self.btn_restart.draw(screen)

    def handle_event(self, event):
        self.btn_back.handle_event(event)
        self.btn_restart.handle_event(event)

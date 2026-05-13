import pygame
import numpy as np
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, WHITE, GRAY
from view.components import Button
from model.hmm import STATE_NAMES, STATE_COLORS
from graphs import create_pie_chart, fig_to_surface


class SummaryScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_stat = pygame.font.Font(None, 24)
        self.font_val = pygame.font.Font(None, 28)
        self.font_btn = pygame.font.Font(None, 26)

        self.btn_next = Button(
            (1000, 640, 200, 50),
            "Siguiente", self.font_btn,
            ACCENT_COLOR, ACCENT_HOVER, callback=self.go_next
        )
        self.btn_back = Button(
            (80, 640, 180, 50),
            "Volver", self.font_btn,
            (60, 60, 80), (80, 80, 110), callback=self.go_back
        )

        self.chart_surface = None

    def go_next(self):
        self.controller.switch_to(4)

    def go_back(self):
        self.controller.switch_to(2)

    def on_enter(self):
        result = self.controller.simulation_result
        if not result or result.n == 0:
            return

        counts = [0, 0, 0]
        for o in result.states:
            counts[o] += 1

        distribution = [c / result.n * 100 for c in counts]

        cached = self.controller.chart_cache.get("summary")
        if cached:
            self.chart_surface = cached
        else:
            fig = create_pie_chart(
                distribution,
                [f"{STATE_NAMES[i]} ({counts[i]})" for i in range(3)],
                STATE_COLORS,
                "Distribución de Sentimientos"
            )
            self.chart_surface = fig_to_surface(fig)
            import matplotlib.pyplot as plt
            plt.close(fig)

        self.counts = counts
        self.distribution_pct = distribution
        self.total_tweets = result.n

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Resumen de la Simulación", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)

        if self.chart_surface:
            chart_rect = self.chart_surface.get_rect(center=(400, 380))
            screen.blit(self.chart_surface, chart_rect)

        stats_x = 750
        draw_text(screen, "Estadísticas", self.font_title, TEXT_COLOR,
                  stats_x + 100, 100, center=True)

        stat_items = [
            ("Total tweets:", str(self.total_tweets), WHITE),
            ("Positivos:", f"{self.counts[0]} ({self.distribution_pct[0]:.1f}%)", STATE_COLORS[0]),
            ("Neutrales:", f"{self.counts[1]} ({self.distribution_pct[1]:.1f}%)", STATE_COLORS[1]),
            ("Negativos:", f"{self.counts[2]} ({self.distribution_pct[2]:.1f}%)", STATE_COLORS[2]),
        ]

        result = self.controller.simulation_result
        if result and result.states:
            transitions = {}
            for i in range(len(result.states) - 1):
                key = (result.states[i], result.states[i + 1])
                transitions[key] = transitions.get(key, 0) + 1

            most_common = max(transitions, key=transitions.get) if transitions else (0, 0)
            stat_items.append((
                "Transición más común:",
                f"{STATE_NAMES[most_common[0]]} ---> {STATE_NAMES[most_common[1]]}",
                GRAY
            ))

        for i, (label, value, color) in enumerate(stat_items):
            y = 170 + i * 55
            draw_text(screen, label, self.font_stat, GRAY, stats_x, y)
            draw_text(screen, str(value), self.font_val, color, stats_x, y + 25)

        self.btn_back.draw(screen)
        self.btn_next.draw(screen)

    def handle_event(self, event):
        self.btn_back.handle_event(event)
        self.btn_next.handle_event(event)

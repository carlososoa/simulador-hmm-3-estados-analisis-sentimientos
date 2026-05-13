import pygame
import math
from view.screen import (
    Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER,
    GREEN, YELLOW, RED, WHITE, GRAY, SCREEN_W, SCREEN_H
)
from view.components import Button
from model.hmm import STATE_NAMES, STATE_EMOJIS, STATE_COLORS
from words import POSITIVE_WORDS, NEUTRAL_WORDS, NEGATIVE_WORDS

POS_X, NEU_X, NEG_X = 250, 640, 1030
CIRCLES_Y = 250
CIRCLES_X = [POS_X, NEU_X, NEG_X]
CIRCLE_R = 70

ARROW_Y_ABOVE = 218
ARROW_Y_BELOW = 282

SPEED_OPTIONS = [
    ("Rápido", 5),
    ("Normal", 300),
    ("Lento", 2000),
]
WORD_LISTS = [POSITIVE_WORDS, NEUTRAL_WORDS, NEGATIVE_WORDS]

ITEM_H = 26
LIST_X = 40
LIST_W = 1200
LIST_Y = 520
LIST_H = 110
VISIBLE_ITEMS = LIST_H // ITEM_H


class SimulationScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_progress = pygame.font.Font(None, 30)
        self.font_tweet_small = pygame.font.Font(None, 20)
        self.font_btn = pygame.font.Font(None, 26)
        self.font_emoji = pygame.font.Font(None, 72)
        self.font_word = pygame.font.Font(None, 36)
        self.font_tweet_text = pygame.font.Font(None, 26)
        self.font_arrow = pygame.font.Font(None, 22)
        self.font_state_label = pygame.font.Font(None, 16)

        self.speed_btns = []
        for i, (label, _) in enumerate(SPEED_OPTIONS):
            btn = Button(
                (20 + i * 85, 30, 80, 28), label, self.font_btn,
                (60, 60, 80), (80, 80, 110),
                callback=lambda i=i: self._set_speed(i)
            )
            self.speed_btns.append(btn)

        self.btn_results = Button(
            (540, 650, 200, 50),
            "Ver Resultados", self.font_btn,
            (0, 150, 80), (0, 190, 100),
            callback=self.go_summary
        )

        self.reset()

    def reset(self):
        self.current_index = -1
        self.total = 0
        self.speed_index = 1
        self.delay = SPEED_OPTIONS[self.speed_index][1]
        self.last_time = 0
        self.running = False
        self.done = False
        self.scroll = 0

    def _set_speed(self, idx):
        self.speed_index = idx
        self.delay = SPEED_OPTIONS[idx][1]

    def go_summary(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from graphs import (
            create_pie_chart, create_step_chart, create_line_chart,
            create_sequence_bar_charts, create_confusion_matrix,
            create_convergence_chart, fig_to_surface
        )
        from model.hmm import STATE_NAMES, STATE_COLORS, OBS_NAMES

        result = self.controller.simulation_result
        hmm = self.controller.hmm
        cache = {}

        def loading(msg):
            self.controller.screen.fill(BG_COLOR)
            draw_text(self.controller.screen, "Generando gráficos...", self.font_progress,
                      TEXT_COLOR, SCREEN_W // 2, 300, center=True)
            draw_text(self.controller.screen, msg, self.font_progress,
                      ACCENT_COLOR, SCREEN_W // 2, 340, center=True)
            pygame.display.flip()
            pygame.event.pump()

        loading("Resumen... (1/6)")
        counts = [0, 0, 0]
        for s in result.states:
            counts[s] += 1
        fig = create_pie_chart(
            [c / result.n * 100 for c in counts],
            [f"{STATE_NAMES[i]} ({counts[i]})" for i in range(3)],
            STATE_COLORS, "Distribución de Sentimientos"
        )
        cache["summary"] = fig_to_surface(fig)
        plt.close(fig)

        loading("Tendencia... (2/6)")
        fig = create_step_chart(
            np.array(result.states), STATE_NAMES, STATE_COLORS,
            "Evolución Temporal del Sentimiento", "Número de Tweet", "Sentimiento"
        )
        cache["trend"] = fig_to_surface(fig)
        plt.close(fig)

        loading("Vector estacionario... (3/6)")
        fig = create_line_chart(
            np.array(result.vectors).T, STATE_NAMES, STATE_COLORS,
            "Evolución del Vector Estacionario", "Iteración (k)", "Probabilidad"
        )
        cache["stationary"] = fig_to_surface(fig)
        plt.close(fig)

        loading("Convergencia empírica... (4/6)")
        theoretical = hmm.stationary_distribution()
        n = result.n
        cum_counts = np.zeros((3, n), dtype=float)
        for k in range(n):
            if k == 0:
                cum_counts[result.states[k], k] = 1.0
            else:
                cum_counts[:, k] = cum_counts[:, k - 1]
                cum_counts[result.states[k], k] += 1.0
        fig = create_convergence_chart(
            cum_counts / np.arange(1, n + 1), theoretical,
            STATE_NAMES, STATE_COLORS,
            "Convergencia de Probabilidades Empíricas", "Iteración", "Probabilidad"
        )
        cache["convergence"] = fig_to_surface(fig)
        plt.close(fig)

        loading("Secuencia de estados... (5/6)")
        fig = create_sequence_bar_charts(
            np.array(result.states), np.array(result.observations),
            STATE_NAMES, OBS_NAMES, STATE_COLORS, STATE_COLORS,
            "Secuencia de Estados y Observaciones"
        )
        cache["barchart"] = fig_to_surface(fig)
        plt.close(fig)

        loading("Matriz de confusión... (6/6)")
        matrix = np.zeros((3, 3), dtype=int)
        for s, o in zip(result.states, result.observations):
            matrix[s, o] += 1
        fig = create_confusion_matrix(
            matrix, STATE_NAMES, OBS_NAMES,
            "Matriz de Confusión: Estados vs Observaciones"
        )
        cache["confusion"] = fig_to_surface(fig)
        plt.close(fig)

        self.controller.chart_cache = cache
        self.controller.switch_to(3)

    def on_enter(self):
        result = self.controller.simulation_result
        if result and result.n > 0:
            if self.controller.new_simulation:
                self.controller.new_simulation = False
                self.controller.chart_cache = {}
                self.total = result.n
                self.current_index = -1
                self.running = True
                self.done = False
                self.scroll = 0

                self.speed_index = 1
                self.delay = SPEED_OPTIONS[1][1]

                self.last_time = pygame.time.get_ticks()

    def update(self):
        if self.running and not self.done:
            now = pygame.time.get_ticks()
            if now - self.last_time >= self.delay:
                self.current_index += 1
                self.last_time = now
                self.scroll = max(0, self.current_index + 1 - VISIBLE_ITEMS)
                if self.current_index >= self.total - 1:
                    self.done = True
                    self.running = False

    def _extract_word(self, tweet, obs_idx):
        for word in WORD_LISTS[obs_idx]:
            if word in tweet.lower():
                return word
        return ""

    def _circle_edge(self, cx, cy, angle_deg):
        a = math.radians(angle_deg)
        return (cx + CIRCLE_R * math.cos(a), cy + CIRCLE_R * math.sin(a))

    def _arrowhead(self, screen, tip, angle, color, size=10):
        p1 = tip
        p2 = (tip[0] - size * math.cos(angle - 0.4),
              tip[1] - size * math.sin(angle - 0.4))
        p3 = (tip[0] - size * math.cos(angle + 0.4),
              tip[1] - size * math.sin(angle + 0.4))
        pygame.draw.polygon(screen, color, [p1, p2, p3])

    def _self_loop(self, screen, cx, cy, color, prob):
        arc_cx, arc_cy = cx, cy - CIRCLE_R - 5
        arc_r = 32
        start_a = math.radians(210)
        stop_a = math.radians(330)

        rect = pygame.Rect(arc_cx - arc_r, arc_cy - arc_r, arc_r * 2, arc_r * 2)
        pygame.draw.arc(screen, color, rect, start_a, stop_a, 3)

        ex = arc_cx + arc_r * math.cos(stop_a)
        ey = arc_cy + arc_r * math.sin(stop_a)
        self._arrowhead(screen, (ex, ey), stop_a + math.pi / 2, color, 8)

        draw_text(screen, f"{prob:.1f}", self.font_arrow, color,
                  arc_cx, arc_cy - arc_r - 14, center=True)

    def _straight_arrow(self, screen, x1, x2, y, color, prob, rev=False):
        left = min(x1, x2) + CIRCLE_R
        right = max(x1, x2) - CIRCLE_R
        if rev:
            draw_from, draw_to = right, left
            angle = math.pi
        else:
            draw_from, draw_to = left, right
            angle = 0

        pygame.draw.line(screen, color, (draw_from, y), (draw_to, y), 3)
        self._arrowhead(screen, (draw_to, y), angle, color, 8)

        mx = (draw_from + draw_to) // 2
        draw_text(screen, f"{prob:.1f}", self.font_arrow, color,
                  mx, y - 16, center=True)

    def _curved_arrow(self, screen, from_idx, to_idx, prob, color, above=True):
        fx = CIRCLES_X[from_idx]
        tx = CIRCLES_X[to_idx]

        if above:
            p1 = self._circle_edge(fx, CIRCLES_Y, 330)
            mid_y = CIRCLES_Y - CIRCLE_R - 60
            p3 = self._circle_edge(tx, CIRCLES_Y, 210)
        else:
            p1 = self._circle_edge(fx, CIRCLES_Y, 30)
            mid_y = CIRCLES_Y + CIRCLE_R + 60
            p3 = self._circle_edge(tx, CIRCLES_Y, 150)

        p2 = ((p1[0] + p3[0]) // 2, mid_y)
        pygame.draw.lines(screen, color, False, [p1, p2, p3], 3)

        seg_angle = math.atan2(p3[1] - p2[1], p3[0] - p2[0])
        self._arrowhead(screen, p3, seg_angle, color, 8)

        draw_text(screen, f"{prob:.1f}", self.font_arrow, color,
                  p2[0], p2[1] - 16, center=True)

    def _glow_circle(self, screen, cx, cy, color, active):
        if active:
            for i in range(4, 0, -1):
                r = CIRCLE_R + i * 8
                surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                alpha = max(0, 60 - i * 12)
                pygame.draw.circle(surf, (*color, alpha), (r, r), r)
                screen.blit(surf, (cx - r, cy - r))

        pygame.draw.circle(screen, (30, 36, 56), (cx, cy), CIRCLE_R)
        thickness = 4 if active else 2
        pygame.draw.circle(screen, color, (cx, cy), CIRCLE_R, thickness)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        result = self.controller.simulation_result

        if not result or result.n == 0:
            draw_text(screen, "No hay datos de simulación", self.font_progress,
                      GRAY, SCREEN_W // 2, SCREEN_H // 2, center=True)
            return

        if self.current_index < 0 and not self.running:
            self.current_index = 0
            self.running = False
            self.done = True

        progress = (self.current_index + 1) / self.total if self.current_index >= 0 else 0

        for i, btn in enumerate(self.speed_btns):
            active = i == self.speed_index
            btn.color = ACCENT_COLOR if active else (60, 60, 80)
            btn.hover_color = ACCENT_HOVER if active else (80, 80, 110)
            btn.draw(screen)

        bar_x = 280
        bar_w = 860
        pygame.draw.rect(screen, (40, 44, 64), (bar_x, 30, bar_w, 28), border_radius=5)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            bar_color = GREEN if progress >= 1.0 else ACCENT_COLOR
            pygame.draw.rect(screen, bar_color, (bar_x, 30, fill_w, 28), border_radius=5)
        pygame.draw.rect(screen, (80, 84, 104), (bar_x, 30, bar_w, 28), 2, border_radius=5)

        status = "Simulación completada" if self.done else "Simulando..."
        prog_text = f"{status}  {self.current_index + 1} / {self.total} tweets"
        draw_text(screen, prog_text, self.font_progress,
                  WHITE if self.done else TEXT_COLOR, SCREEN_W // 2, 18, center=True)

        if self.current_index < 0:
            return

        active_state = result.states[self.current_index]

        A = self.controller.hmm.A

        for i in range(3):
            self._self_loop(screen, CIRCLES_X[i], CIRCLES_Y,
                            STATE_COLORS[i], A[i, i])

        self._straight_arrow(screen, POS_X, NEU_X, ARROW_Y_ABOVE,
                             STATE_COLORS[0], A[0, 1])
        self._straight_arrow(screen, POS_X, NEU_X, ARROW_Y_BELOW,
                             STATE_COLORS[1], A[1, 0], rev=True)

        self._straight_arrow(screen, NEU_X, NEG_X, ARROW_Y_ABOVE,
                             STATE_COLORS[1], A[1, 2])
        self._straight_arrow(screen, NEU_X, NEG_X, ARROW_Y_BELOW,
                             STATE_COLORS[2], A[2, 1], rev=True)

        self._curved_arrow(screen, 0, 2, A[0, 2],
                           STATE_COLORS[0], above=True)
        self._curved_arrow(screen, 2, 0, A[2, 0],
                           STATE_COLORS[2], above=False)

        for i in range(3):
            cx = CIRCLES_X[i]
            color = STATE_COLORS[i]
            active = (i == active_state)
            self._glow_circle(screen, cx, CIRCLES_Y, color, active)

            draw_text(screen, STATE_EMOJIS[i], self.font_emoji, WHITE,
                      cx, CIRCLES_Y - 8, center=True)
            draw_text(screen, STATE_NAMES[i], self.font_state_label, GRAY,
                      cx, CIRCLES_Y + CIRCLE_R + 10, center=True)

        obs = result.observations[self.current_index]
        obs_label = ["palabra positiva", "palabra neutra", "palabra negativa"][obs]
        emitted_word = self._extract_word(result.tweets[self.current_index], obs)
        word_color = STATE_COLORS[active_state]

        word_box_y = CIRCLES_Y + CIRCLE_R + 75
        word_display = f"{obs_label}: «{emitted_word}»" if emitted_word else obs_label

        pygame.draw.rect(screen, (30, 36, 60),
                         (400, word_box_y, 480, 40), border_radius=8)
        pygame.draw.rect(screen, word_color,
                         (400, word_box_y, 480, 40), 2, border_radius=8)
        draw_text(screen, word_display, self.font_word, word_color,
                  640, word_box_y + 20, center=True)

        tweet_y = word_box_y + 55
        tweet = result.tweets[self.current_index]
        draw_text(screen, f'💬 {tweet}', self.font_tweet_text, TEXT_COLOR,
                  640, tweet_y, center=True)

        pygame.draw.rect(screen, (26, 32, 52),
                         (LIST_X - 5, LIST_Y - 5, LIST_W + 10, LIST_H + 10),
                         border_radius=8)

        start_idx = max(0, self.scroll)
        end_idx = min(self.current_index + 1, start_idx + VISIBLE_ITEMS)

        for i in range(start_idx, end_idx):
            st = result.states[i]
            tweet = result.tweets[i]
            color = STATE_COLORS[st]
            y = LIST_Y + (i - start_idx) * ITEM_H

            if i == self.current_index and self.done:
                pygame.draw.rect(screen, (40, 46, 70),
                                 (LIST_X, y, LIST_W, ITEM_H - 2))
            elif i % 2 == 0:
                pygame.draw.rect(screen, (30, 36, 56),
                                 (LIST_X, y, LIST_W, ITEM_H - 2))

            pygame.draw.rect(screen, color,
                             (LIST_X + 5, y + 3, 6, ITEM_H - 8), border_radius=3)
            draw_text(screen, f"#{i + 1}", self.font_tweet_small,
                      GRAY, LIST_X + 20, y + 2)
            draw_text(screen, STATE_EMOJIS[st], self.font_tweet_small,
                      TEXT_COLOR, LIST_X + 55, y + 2)
            draw_text(screen, tweet, self.font_tweet_small,
                      TEXT_COLOR, LIST_X + 130, y + 2)

        if self.done:
            self.btn_results.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.current_index >= 0:
            self.scroll -= event.y
            max_scroll = max(0, self.current_index + 1 - VISIBLE_ITEMS)
            self.scroll = max(0, min(self.scroll, max_scroll))

        for btn in self.speed_btns:
            btn.handle_event(event)

        if self.done:
            self.btn_results.handle_event(event)

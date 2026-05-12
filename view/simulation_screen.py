import pygame
import math
from view.screen import (
    Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER,
    GREEN, YELLOW, RED, WHITE, GRAY, SCREEN_W, SCREEN_H
)
from view.components import Button
from model.hmm import STATE_NAMES, STATE_EMOJIS, STATE_COLORS

POS_X, NEU_X, NEG_X = 250, 640, 1030
CIRCLES_Y = 250
CIRCLES_X = [POS_X, NEU_X, NEG_X]
CIRCLE_R = 70

ARROW_Y_ABOVE = 218
ARROW_Y_BELOW = 282

TRANS_PROBS = {
    (0, 0): 0.6, (0, 1): 0.3, (0, 2): 0.1,
    (1, 0): 0.2, (1, 1): 0.6, (1, 2): 0.2,
    (2, 0): 0.1, (2, 1): 0.3, (2, 2): 0.6,
}

ITEM_H = 26
LIST_X = 40
LIST_W = 1200
LIST_Y = 490
LIST_H = 130
VISIBLE_ITEMS = LIST_H // ITEM_H


class SimulationScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_progress = pygame.font.Font(None, 30)
        self.font_tweet_small = pygame.font.Font(None, 20)
        self.font_btn = pygame.font.Font(None, 26)
        self.font_emoji = pygame.font.Font(None, 72)
        self.font_word = pygame.font.Font(None, 40)
        self.font_tweet_text = pygame.font.Font(None, 26)
        self.font_arrow = pygame.font.Font(None, 22)
        self.font_state_label = pygame.font.Font(None, 16)

        self.btn_results = Button(
            (540, 640, 200, 50),
            "Ver Resultados", self.font_btn,
            (0, 150, 80), (0, 190, 100),
            callback=self.go_summary
        )

        self.reset()

    def reset(self):
        self.current_index = -1
        self.total = 0
        self.delay = 200
        self.last_time = 0
        self.running = False
        self.done = False
        self.scroll = 0

    def go_summary(self):
        self.controller.switch_to(3)

    def on_enter(self):
        result = self.controller.simulation_result
        if result and result.n > 0:
            self.total = result.n
            self.current_index = -1
            self.running = True
            self.done = False
            self.scroll = 0

            if self.total <= 10:
                self.delay = 300
            elif self.total <= 100:
                self.delay = 40
            else:
                self.delay = 5

            self.last_time = pygame.time.get_ticks()

    def update(self):
        if self.running and not self.done:
            now = pygame.time.get_ticks()
            if now - self.last_time >= self.delay:
                self.current_index += 1
                self.last_time = now
                if self.current_index >= self.total - 1:
                    self.done = True
                    self.running = False

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

        pygame.draw.rect(screen, (40, 44, 64), (140, 30, 1000, 28), border_radius=5)
        fill_w = int(1000 * progress)
        if fill_w > 0:
            bar_color = GREEN if progress >= 1.0 else ACCENT_COLOR
            pygame.draw.rect(screen, bar_color, (140, 30, fill_w, 28), border_radius=5)
        pygame.draw.rect(screen, (80, 84, 104), (140, 30, 1000, 28), 2, border_radius=5)

        status = "Simulación completada" if self.done else "Simulando..."
        prog_text = f"{status}  {self.current_index + 1} / {self.total} tweets"
        draw_text(screen, prog_text, self.font_progress,
                  WHITE if self.done else TEXT_COLOR, SCREEN_W // 2, 18, center=True)

        if self.current_index < 0:
            return

        active_state = result.states[self.current_index]

        for i in range(3):
            self._self_loop(screen, CIRCLES_X[i], CIRCLES_Y,
                            STATE_COLORS[i], TRANS_PROBS[(i, i)])

        self._straight_arrow(screen, POS_X, NEU_X, ARROW_Y_ABOVE,
                             STATE_COLORS[0], TRANS_PROBS[(0, 1)])
        self._straight_arrow(screen, POS_X, NEU_X, ARROW_Y_BELOW,
                             STATE_COLORS[1], TRANS_PROBS[(1, 0)], rev=True)

        self._straight_arrow(screen, NEU_X, NEG_X, ARROW_Y_ABOVE,
                             STATE_COLORS[1], TRANS_PROBS[(1, 2)])
        self._straight_arrow(screen, NEU_X, NEG_X, ARROW_Y_BELOW,
                             STATE_COLORS[2], TRANS_PROBS[(2, 1)], rev=True)

        self._curved_arrow(screen, 0, 2, TRANS_PROBS[(0, 2)],
                           STATE_COLORS[0], above=True)
        self._curved_arrow(screen, 2, 0, TRANS_PROBS[(2, 0)],
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
        obs_name = ["palabra positiva", "palabra neutra", "palabra negativa"][obs]
        word_box_y = CIRCLES_Y + CIRCLE_R + 40
        word_color = STATE_COLORS[active_state]

        pygame.draw.rect(screen, (30, 36, 60),
                         (440, word_box_y, 400, 40), border_radius=8)
        pygame.draw.rect(screen, word_color,
                         (440, word_box_y, 400, 40), 2, border_radius=8)
        draw_text(screen, f'"{obs_name}"', self.font_word, word_color,
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

        if self.done:
            self.btn_results.handle_event(event)

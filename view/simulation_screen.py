import pygame
from view.screen import (
    Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER,
    GREEN, YELLOW, RED, WHITE, GRAY, SCREEN_W, SCREEN_H
)
from view.components import Button
from model.hmm import STATE_NAMES, STATE_EMOJIS, STATE_COLORS


ITEM_H = 28
LIST_X = 40
LIST_W = 1200
LIST_Y = 230
LIST_H = 450
VISIBLE_ITEMS = LIST_H // ITEM_H


class SimulationScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_progress = pygame.font.Font(None, 30)
        self.font_tweet = pygame.font.Font(None, 22)
        self.font_btn = pygame.font.Font(None, 26)
        self.font_current_num = pygame.font.Font(None, 20)
        self.font_current_text = pygame.font.Font(None, 32)
        self.font_current_state = pygame.font.Font(None, 24)

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

        pygame.draw.rect(screen, (40, 44, 64), (140, 55, 1000, 28), border_radius=5)
        fill_w = int(1000 * progress)
        if fill_w > 0:
            color = GREEN if progress >= 1.0 else ACCENT_COLOR
            pygame.draw.rect(screen, color, (140, 55, fill_w, 28), border_radius=5)
        pygame.draw.rect(screen, (80, 84, 104), (140, 55, 1000, 28), 2, border_radius=5)

        status = "Simulación completada" if self.done else "Simulando..."
        prog_text = f"{status}  {self.current_index + 1} / {self.total} tweets"
        draw_text(screen, prog_text, self.font_progress,
                  WHITE if self.done else TEXT_COLOR, SCREEN_W // 2, 42, center=True)

        if self.current_index >= 0:
            idx = self.current_index
            st = result.states[idx]
            tweet = result.tweets[idx]
            color = STATE_COLORS[st]

            pygame.draw.rect(screen, (30, 36, 60), (340, 100, 600, 110), border_radius=10)
            pygame.draw.rect(screen, color, (340, 100, 600, 110), 2, border_radius=10)

            state_text = f"{STATE_EMOJIS[st]}  {STATE_NAMES[st]}"
            draw_text(screen, f"Tweet #{idx + 1}", self.font_current_num, GRAY, 360, 110)
            draw_text(screen, state_text, self.font_current_state, color, 640, 135, center=True)
            draw_text(screen, f'"{tweet}"', self.font_current_text, WHITE, 640, 175, center=True)

        pygame.draw.rect(screen, (26, 32, 52), (LIST_X - 5, LIST_Y - 5, LIST_W + 10, LIST_H + 10),
                         border_radius=8)

        start_idx = max(0, self.scroll)
        end_idx = min(self.current_index + 1, start_idx + VISIBLE_ITEMS)

        for i in range(start_idx, end_idx):
            st = result.states[i]
            tweet = result.tweets[i]
            color = STATE_COLORS[st]
            y = LIST_Y + (i - start_idx) * ITEM_H

            if i == self.current_index and self.done:
                pygame.draw.rect(screen, (40, 46, 70), (LIST_X, y, LIST_W, ITEM_H - 2))
            elif i % 2 == 0:
                pygame.draw.rect(screen, (30, 36, 56), (LIST_X, y, LIST_W, ITEM_H - 2))

            pygame.draw.rect(screen, color, (LIST_X + 5, y + 4, 6, ITEM_H - 10), border_radius=3)
            draw_text(screen, f"#{i + 1}", self.font_tweet, GRAY, LIST_X + 20, y + 4)
            draw_text(screen, STATE_EMOJIS[st], self.font_tweet, TEXT_COLOR, LIST_X + 60, y + 4)
            draw_text(screen, tweet, self.font_tweet, TEXT_COLOR, LIST_X + 150, y + 4)

        if self.done:
            self.btn_results.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.current_index >= 0:
            self.scroll -= event.y
            max_scroll = max(0, self.current_index + 1 - VISIBLE_ITEMS)
            self.scroll = max(0, min(self.scroll, max_scroll))

        if self.done:
            self.btn_results.handle_event(event)

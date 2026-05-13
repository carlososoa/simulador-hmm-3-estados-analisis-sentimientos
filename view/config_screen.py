import pygame
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER, WHITE, GRAY
from view.components import Button, MatrixGrid
from model.hmm import STATE_NAMES
from words import generate_tweet


class ConfigScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 36)
        self.font_cell = pygame.font.Font(None, 22)
        self.font_btn = pygame.font.Font(None, 26)
        self.font_label = pygame.font.Font(None, 22)
        self.font_warn = pygame.font.Font(None, 20)

        self.tweet_options = [10, 100, 500, 1000, 3500]
        self.selected_tweets = 10

        self.tweet_buttons = []
        for i, n in enumerate(self.tweet_options):
            btn = Button(
                (150 + i * 200, 390, 180, 45),
                f"{n} tweets", self.font_btn,
                (60, 60, 80), (80, 80, 110),
                callback=lambda count=n: self.select_tweet_count(count)
            )
            self.tweet_buttons.append(btn)

        self.btn_start = Button(
            (540, 475, 200, 50),
            "Iniciar Simulación", self.font_btn,
            (0, 150, 80), (0, 190, 100),
            callback=self.start_simulation
        )

        self.matrices_initialized = False
        self.warning_text = ""

    def select_tweet_count(self, count):
        self.selected_tweets = count

    def start_simulation(self):
        self.deactivate_all()
        A = self.matrix_A.get_values()
        B = self.matrix_B.get_values()
        pi_vec = self.matrix_pi.get_values()[0]

        self.controller.hmm.set_matrices(A, B, pi_vec)
        result = self.controller.hmm.generate_sequence(
            self.selected_tweets, generate_tweet
        )
        self.controller.simulation_result = result
        self.controller.switch_to(2)

    def deactivate_all(self):
        if hasattr(self, 'matrix_A'):
            self.matrix_A.deactivate_all()
            self.matrix_B.deactivate_all()
            self.matrix_pi.deactivate_all()

    def on_enter(self):
        hmm = self.controller.hmm
        self.matrix_A = MatrixGrid(
            50, 125, "A (Matriz de Transición)",
            3, 3, hmm.A.tolist(),
            ["S1", "S2", "S3"], ["S1", "S2", "S3"],
            self.font_cell
        )
        self.matrix_B = MatrixGrid(
            540, 125, "B (Matriz de Emisión)",
            3, 3, hmm.B.tolist(),
            ["S1", "S2", "S3"], ["v1", "v2", "v3"],
            self.font_cell
        )
        self.matrix_pi = MatrixGrid(
            350, 275, "π (Distribución Inicial)",
            1, 3, [hmm.pi.tolist()],
            ["π"], ["S1", "S2", "S3"],
            self.font_cell
        )
        self.matrices_initialized = True
        self.warning_text = ""

    def draw(self, screen):
        screen.fill(BG_COLOR)
        draw_text(screen, "Configuración de la Simulación", self.font_title,
                  TEXT_COLOR, 640, 35, center=True)

        y_info = 75
        draw_text(screen, "Estados ocultos: 3 (Positivo, Neutral, Negativo)",
                  self.font_label, GRAY, 50, y_info)
        draw_text(screen, "Observaciones: 3 (palabra positiva, neutra, negativa)",
                  self.font_label, GRAY, 50, y_info + 22)

        if self.matrices_initialized:
            self.matrix_A.draw(screen)
            self.matrix_B.draw(screen)
            self.matrix_pi.draw(screen)

        draw_text(screen, "Número de tweets a simular:", self.font_label,
                  TEXT_COLOR, 640, 360, center=True)

        for i, btn in enumerate(self.tweet_buttons):
            if self.tweet_options[i] == self.selected_tweets:
                btn.color = ACCENT_COLOR
                btn.hover_color = ACCENT_HOVER
            else:
                btn.color = (60, 60, 80)
                btn.hover_color = (80, 80, 110)
            btn.draw(screen)

        self.btn_start.draw(screen)

        if self.warning_text:
            draw_text(screen, self.warning_text, self.font_warn,
                      (255, 200, 100), 640, 465, center=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.matrix_A.handle_event(event)
            self.matrix_B.handle_event(event)
            self.matrix_pi.handle_event(event)

        self.btn_start.handle_event(event)
        for btn in self.tweet_buttons:
            btn.handle_event(event)

        if self.matrices_initialized:
            self.matrix_A.handle_event(event)
            self.matrix_B.handle_event(event)
            self.matrix_pi.handle_event(event)

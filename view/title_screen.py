import pygame
from view.screen import Screen, draw_text, BG_COLOR, TEXT_COLOR, ACCENT_COLOR, ACCENT_HOVER
from view.components import Button


class TitleScreen(Screen):
    def __init__(self, controller):
        super().__init__(controller)
        self.font_title = pygame.font.Font(None, 48)
        self.font_sub = pygame.font.Font(None, 28)
        self.font_names = pygame.font.Font(None, 30)
        self.font_btn = pygame.font.Font(None, 28)

        self.btn_next = Button(
            (540, 600, 200, 55), "Siguiente", self.font_btn,
            ACCENT_COLOR, ACCENT_HOVER, callback=self.go_next
        )

    def go_next(self):
        self.controller.switch_to(1)

    def draw(self, screen):
        screen.fill(BG_COLOR)

        draw_text(screen, "Simulador HMM", self.font_title, TEXT_COLOR,
                  640, 120, center=True)
        draw_text(screen, "Análisis de Sentimientos en Redes Sociales",
                  self.font_sub, TEXT_COLOR, 640, 180, center=True)

        draw_text(screen, "Integrantes:", self.font_names, TEXT_COLOR,
                  640, 290, center=True)

        names = [
            "Estefania Martinez Guzman",
            "Valentina Pérez Flórez",
            "Carlos Andrés Osorio Agudelo"
        ]
        for i, name in enumerate(names):
            draw_text(screen, name, self.font_names, (180, 200, 255),
                      640, 350 + i * 45, center=True)

        self.btn_next.draw(screen)

    def handle_event(self, event):
        self.btn_next.handle_event(event)

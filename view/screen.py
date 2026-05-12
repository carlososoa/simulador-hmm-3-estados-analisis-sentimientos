import pygame

BG_COLOR = (18, 22, 40)
PANEL_COLOR = (26, 32, 52)
TEXT_COLOR = (230, 230, 245)
ACCENT_COLOR = (66, 133, 244)
ACCENT_HOVER = (100, 160, 255)
GREEN = (76, 175, 80)
YELLOW = (255, 193, 7)
RED = (244, 67, 54)
WHITE = (255, 255, 255)
GRAY = (100, 100, 120)

SCREEN_W = 1280
SCREEN_H = 720


def draw_text(screen, text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)


class Screen:
    def __init__(self, controller):
        self.controller = controller

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

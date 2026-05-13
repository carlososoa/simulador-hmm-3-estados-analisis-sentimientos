import pygame
from model.hmm import HMM
from view.screen import SCREEN_W, SCREEN_H
from view.title_screen import TitleScreen
from view.config_screen import ConfigScreen
from view.simulation_screen import SimulationScreen
from view.summary_screen import SummaryScreen
from view.trend_screen import TrendScreen
from view.stationary_screen import StationaryScreen
from view.bar_chart_screen import BarChartScreen
from view.confusion_screen import ConfusionScreen


class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Simulador HMM - Análisis de Sentimientos en Redes Sociales")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_index = 0

        self.hmm = HMM()
        self.simulation_result = None

        self.screens = [
            TitleScreen(self),
            ConfigScreen(self),
            SimulationScreen(self),
            SummaryScreen(self),
            TrendScreen(self),
            StationaryScreen(self),
            BarChartScreen(self),
            ConfusionScreen(self),
        ]

    def switch_to(self, index):
        if 0 <= index < len(self.screens):
            self.screens[self.current_index].on_exit()
            self.current_index = index
            self.screens[self.current_index].on_enter()

    def run(self):
        self.screens[0].on_enter()

        while self.running:
            current = self.screens[self.current_index]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                current.handle_event(event)

            current.update()
            current.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

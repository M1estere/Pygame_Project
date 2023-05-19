import pygame

from misc.settings import *

class Menu():
    def __init__(self, game):
        self.game = game

        self.mid_width = WIDTH // 2
        self.mid_height = HEIGTH // 2

        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 200, 200)

        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))

        pygame.display.update()
        self.game.reset_keys()
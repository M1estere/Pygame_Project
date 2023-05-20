import pygame, sys

from misc.settings import *

from ui.main_menu import MainMenu
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        self.display = pygame.Surface((WIDTH, HEIGTH))
        self.window = pygame.display.set_mode((WIDTH, HEIGTH))
        self.font_name = 'joystix.ttf'
        
        self.open_main_menu()

        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

    def game_loop(self):
        while self.playing:
            self.check_events()

            if self.START_KEY: self.playing = False
            self.display.fill('black')

            self.draw_text('Starting game', WIDTH, HEIGTH)

            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

            self.reset_keys()

    def start_level(self):
        self.level = Level()
        self.display.fill(WATER_COLOUR)

    def open_main_menu(self):
        self.reset_keys()

        self.playing = False
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.playing:
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                        self.toggle()

            if not self.playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.START_KEY = True

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.DOWN_KEY = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.UP_KEY = True

    def toggle(self):
        self.level.toggle_menu(self)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, x, y):
        font = pygame.font.Font(UI_FONT, 40)

        text_surface = font.render(text, False, TEXT_COLOUR)
        text_rect = text_surface.get_rect(center = (x, y))

        self.display.blit(text_surface, text_rect)

if __name__ == '__main__':
    game = Game()
    game.curr_menu.display_menu()

    game.game_loop()
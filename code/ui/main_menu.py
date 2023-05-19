from misc.settings import *

from menu import Menu

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'

        self.start_x = self.mid_width
        self.start_y = self.mid_height + 150

        self.quit_x = self.mid_width
        self.quit_y = self.mid_height + 200

        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()

            self.check_input()
            self.game.display.fill('#1b0030')

            self.game.draw_text(GAME_TITLE, WIDTH // 2, 200)
            self.game.draw_text('Start Game', self.start_x, self.start_y)
            self.game.draw_text('Quit Game', self.quit_x, self.quit_y)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.start_level()
            elif self.state == 'Quit':
                pass

            self.run_display = False
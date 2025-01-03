import sys

import pygame

from settings import Settings
# from tilemap import Tilemap
from level_editor import LevelEditor
from text_input import TextInput
from tileset import Tileset

class Game:
    # game states
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.font = pygame.font.SysFont(None, 48)

        self.tileset = Tileset(self)

        self.editor = LevelEditor(self)

        # used for avoiding pressing two objects at once that overlap
        self.ignore_click = False

        # used for blocking player controls when writing to text box
        self.current_text_box = None

        # self.text_input = TextInput(self, pygame.Rect(10, 10, 100, 30),
        #                             24, 'black', 'white')

    def play(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.current_text_box:
                    # pass every key to write in current text box
                    # stop other controls
                    if event.type == pygame.KEYDOWN:
                        self.current_text_box.handle_input(event.key)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # check if clicked outside box and is still writing
                        self.current_text_box.detect_collision()
                self._in_editor_controls(event)

            # not before event loop to avoid bugs
            self.mouse_pressed = pygame.mouse.get_pressed()

            self.screen.fill("white")
            if not self.ignore_click:
                if self.mouse_pressed[0]:
                    self.editor.swap_tile()
            self.editor.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def _in_editor_controls(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.ignore_click:
                success = self.editor.change_tile()
                self.ignore_click = success
        elif event.type == pygame.MOUSEBUTTONUP:
            self.ignore_click = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.editor.is_tileset_shown = not self.editor.is_tileset_shown
            elif event.key == pygame.K_s:
                self.editor.display_save_window = True
                self.editor.file_name_input.detect_collision()
                # self.editor.save_map('test.json')

            if self.editor.display_save_window and event.key == pygame.K_RETURN:
                self.editor.display_save_window = False
                self.editor.save_map(self.editor.file_name_input.text)
                self.editor.file_name_input.text = "Map name"



if __name__ == "__main__":
    game = Game()
    game.play()
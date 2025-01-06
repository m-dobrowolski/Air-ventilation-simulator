import pygame

from level_editor.settings import Settings
from level_editor.level_editor import LevelEditor
from level_editor.tileset import Tileset

class Game:
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

    def play(self):
        game_active = True
        while game_active:
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False

                if self.current_text_box:
                    # pass every key to write in current text box
                    # stop other controls
                    if event.type == pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        is_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                        self.current_text_box.handle_input(event.key, is_shift)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # check if clicked outside box and is still writing
                        self.current_text_box.detect_collision()
                map_path = self._in_editor_controls(event)
                if map_path:
                    pygame.quit()
                    return map_path

            # not before event loop to avoid bugs
            self.mouse_pressed = pygame.mouse.get_pressed()

            self.screen.fill("white")
            if not self.ignore_click and not self.editor.display_save_window:
                if self.mouse_pressed[0]:
                    self.editor.swap_tile()
            self.editor.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _in_editor_controls(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.ignore_click and not self.editor.display_save_window:
                success = self.editor.change_tile()
                self.ignore_click = success
            if self.editor.display_save_window is True:
                self.editor.file_name_input.detect_collision()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.ignore_click = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.editor.is_tileset_shown = not self.editor.is_tileset_shown
            elif event.key == pygame.K_s:
                self.editor.display_save_window = True
                self.editor.file_name_input.set_active()
            elif event.key == pygame.K_ESCAPE:
                if self.editor.display_save_window:
                    self.editor.display_save_window = False
                    self.editor.file_name_input.text = 'Map name'
                    self.editor.file_name_input.set_inactive()


            if self.editor.display_save_window and event.key == pygame.K_RETURN:
                self.editor.display_save_window = False
                map_path = f'level_editor/maps/{self.editor.file_name_input.text}'
                self.editor.save_map(map_path)
                return map_path
        return None

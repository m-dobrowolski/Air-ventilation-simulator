import pygame


class TextInput():
    def __init__(self, game, rect, text_size, text_color, bg_color):
        self.game = game
        self.screen = self.game.screen
        self.rect = rect
        self.text_size = text_size
        self.text_color = text_color
        self.bg_color = bg_color

        self.font = pygame.font.SysFont(None, 48)
        self.text = ''
        self.old_text = ''  # used to minimize times of img generation
        self.img = None
        self.img_rect = None

        self.is_writing = False
        self.is_visible = False
        self.cursor_x = self.rect.x
        self.cursor_index = len(self.text)


    def draw(self):
        # prepare for drawing
        self._prep_text()
        self._calculate_cursor_pos()

        # draw background
        self.screen.fill(self.bg_color, self.rect)

        # draw text
        if self.img:
            self.screen.blit(self.img, self.img_rect)

        # draw cursor
        if self.is_writing:
            y_top = self.img_rect.top
            y_bottom = y_top + self.font.get_height()
            pygame.draw.aaline(self.screen, 'black', (self.cursor_x, y_top),
                               (self.cursor_x, y_bottom))

    def _prep_text(self):
        if self.old_text != self.text:
            self.img = (self.font.render(self.text, True, self.text_color,
                                         self.bg_color))
            self.img_rect = self.img.get_rect()
            self.img_rect.midleft = self.rect.midleft
            self.old_text = self.text

    def _upper(self, key):
        if (key >= pygame.K_a and key <= pygame.K_z):
            return key - 32
        if key == pygame.K_MINUS:
            return 95 # '_'

    def handle_input(self, key, is_shift=False):
        if (
            # Allowed keys
            (key >= pygame.K_a and key <= pygame.K_z) or
            (key >= pygame.K_0 and key <= pygame.K_9) or
            key == pygame.K_SPACE or
            key == pygame.K_PERIOD or
            key == pygame.K_MINUS
        ):
            if is_shift:
                key = self._upper(key)
            self._write_key(key)
        elif key == pygame.K_BACKSPACE:
            self._del_letter()
        elif key == pygame.K_LEFT:
            self._decrement_cursor_index()
        elif key == pygame.K_RIGHT:
            self._increment_cursor_index()

    def _write_key(self, key, upper=False):
        """Writes key from a to z."""
        str_key = chr(key)
        if upper:
            str_key = str_key.upper()

        self.text = (
            self.text[:self.cursor_index] + str_key +
            self.text[self.cursor_index:]
        )
        self._increment_cursor_index()

    def _del_letter(self):
        if self.text:
            self.text = (
                self.text[:self.cursor_index-1] + self.text[self.cursor_index:]
            )
            self._decrement_cursor_index()

    def detect_collision(self):
        """Check if click is on the textbox, set current text box."""
        if self.is_visible:
            if self.rect.collidepoint(self.game.mouse_pos):
                self.game.current_text_box = self
                self.is_writing = True
                self.cursor_index = len(self.text)
                return True

        self.game.current_text_box = None
        self.is_writing = False
        return False

    def set_active(self):
        self.game.current_text_box = self
        self.is_writing = True
        self.cursor_index = len(self.text)

    def set_inactive(self):
        self.game.current_text_box = None
        self.is_writing = False

    def _calculate_cursor_pos(self):
        if self.img_rect is not None:
            self.cursor_x = (
                self.font.size(self.text[:self.cursor_index])[0] +
                self.img_rect.x
            )

    def _increment_cursor_index(self):
        if self.cursor_index < len(self.text):
            self.cursor_index += 1

    def _decrement_cursor_index(self):
        if self.cursor_index > 0:
            self.cursor_index -= 1

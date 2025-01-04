import pygame


class Button:
    def __init__(
            self, screen, rect, text, text_color="white", bg_color="black",
    ):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(None, 48)
        self._prep_msg()

    def _prep_msg(self):
        self.img_text = self.font.render(
            self.text, True, self.text_color, self.bg_color
        )
        self.img_text_rect = self.img_text.get_rect()
        self.img_text_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.img_text, self.img_text_rect)

from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, rect=None, image=None, tile_num=None):
        super().__init__()

        self.rect = rect
        self.image = image
        self.tile_num = tile_num

    def blitme(self, surface):
        if self.image and self.rect:
            surface.blit(self.image, self.rect)

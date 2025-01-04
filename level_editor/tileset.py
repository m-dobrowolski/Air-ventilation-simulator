import pygame


class Tileset:
    def __init__(self, game):
        self.game = game
        self.settings = self.game.settings

        self.file = self.settings.tileset_file
        self.margin = self.settings.tileset_margin
        self.spacing = self.settings.tileset_spacing
        self.size = self.settings.tile_size

        self.num_rows = 0
        self.num_columns = 0

        self.tiles = []

        self.image = pygame.image.load(self.file)
        self.rect = self.image.get_rect()

        self._load()

    def _load(self):
        width, height = self.rect.size
        x0 = y0 = self.margin
        dx, dy = self.size[0] + self.spacing, self.size[1] + self.spacing

        for x in range(x0, width, dx):
            for y in range(y0, height, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

            # count the size of tileset
            if not self.num_rows:
                self.num_rows = len(self.tiles)
            self.num_columns += 1

    def get_tile(self, index):
        if index is None:
            return

        if index >= 0 and index < len(self.tiles):
            return self.tiles[index]

    def blitme(self):
        self.game.screen.blit(self.tiles[18], self.rect)

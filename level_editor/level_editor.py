import pygame
import json

from pygame.sprite import Group
from pygame import Rect

from tile import Tile
from text_input import TextInput

class LevelEditor():
    """A class to create game maps."""

    def __init__(self, game):
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.tileset = self.game.tileset

        self.is_tileset_shown = True

        self.current_tile_num = 1
        self.current_tile_img = self.tileset.get_tile(self.current_tile_num)

        self.tiles = Group()
        self.tileset_displayed = Group()

        self.map = []

        self._gen_tiles()
        self._gen_tileset()


        self.display_save_window = False
        # create save window
        height, width = 150, 400
        self.save_window_rect = Rect(0, 0, width, height)
        self.save_window_rect.center = self.screen_rect.center

        rect = Rect(0, 0, width - 40, 50)
        rect.center = self.screen_rect.center
        rect.y += 20
        self.file_name_input = TextInput(self.game, rect, 36, 'black', 'white')
        self.file_name_input.is_visible = False
        self.file_name_input.text = "Map name"

    def draw(self):
        """Draw level editor features"""

        # draw tiles and green grid
        for tile in self.tiles.sprites():
            pygame.draw.rect(self.screen, 'green', tile.rect, 1)
            tile.blitme(self.screen)

        # draw tileset and red grid
        if self.is_tileset_shown:
            for tile in self.tileset_displayed.sprites():
                tile.blitme(self.screen)
                pygame.draw.rect(self.screen, 'red', tile.rect, 1)

        if self.display_save_window:
            self._draw_save_window()
            self.file_name_input.draw()

    def _gen_tiles(self):
        """Fill the screen with blank tiles"""
        x0, y0 = 0, 0
        width, height = self.settings.tile_size

        for y in range(y0, self.settings.screen_height, height):
            for x in range(x0, self.settings.screen_width, width):
                self.tiles.add(Tile(Rect(x, y, width, height)))

    def swap_tile(self):
        """Swap current tile to the tile selected from tileset."""
        for tile in self.tiles:
            if tile.rect.collidepoint(self.game.mouse_pos):
                # TODO: tile.update() - updates image and tile type
                tile.image = self.current_tile_img
                tile.tile_num = self.current_tile_num
                return True
        return False

    def change_tile(self):
        """Change clicked tile on a map to the current tile."""
        if self.is_tileset_shown:
            for tile in self.tileset_displayed:
                if tile.rect.collidepoint(self.game.mouse_pos):
                    self.current_tile_num = tile.tile_num
                    self.current_tile_img = self.tileset.get_tile(
                        tile.tile_num
                    )
                    return True
        return False

    def _gen_tileset(self):
        """Fill the screen with blank tiles"""
        x0, y0 = 0, 0
        width, height = self.settings.tile_size
        max_x = x0 + self.tileset.num_columns * width
        max_y = y0 + self.tileset.num_rows * height

        tile_num = 0
        for x in range(x0, max_x, width):
            for y in range(y0, max_y, height):
                self.tileset_displayed.add(
                    Tile(
                        Rect(x, y, width, height),
                        self.tileset.get_tile(tile_num),
                        tile_num
                    )
                )
                tile_num += 1

    def save_map(self, path):
        """Convert and save created map to the path."""
        restructured_map = self._restructure_map()

        # invert map so [y][x] starts from left top corner
        map_to_save = json.dumps(restructured_map[::-1], indent=4)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(map_to_save)

    def _restructure_map(self):
        """
        Convert tiles in the pygame.sprite.Group to the map in a list.
        The form is easier to save and read.
        """
        rows = []
        row = []
        for tile in self.tiles.sprites():
            row.append(0 if tile.tile_num is None else tile.tile_num)

            if len(row) == self.settings.tiles_num_border:
                rows.append(row)
                row = []
        return rows

    def _draw_save_window(self):
        # draw background
        self.screen.fill('black', self.save_window_rect)

        # generate text message
        msg_img = self.game.font.render('Save the map', True, 'white', 'black')
        msg_rect = msg_img.get_rect()
        msg_rect.midtop = self.save_window_rect.midtop
        msg_rect.y += 25
        self.screen.blit(msg_img, msg_rect)

        self.file_name_input.is_visible = True





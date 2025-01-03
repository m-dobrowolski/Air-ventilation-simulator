# import json

# from tileset import Tileset


# class Tilemap:
#     def __init__(self, game):
#         self.game = game
#         self.screen = self.game.screen
#         self.settings = self.game.settings

#         self.tileset = Tileset(self.game)
#         self.size = self.tileset.size

#         self.map = self._load_map()

#     def _load_map(self):
#         with open('test.json', 'r', encoding='utf-8') as fh:
#             map_str = fh.read()
#         return json.loads(map_str)

#     def display(self):
#         x0, y0 = 0, 0
#         x, y = x0, y0
#         dx, dy = self.size
#         for row in self.map:
#             for tile_index in row:
#                 if tile_index is not None:
#                     tile = self.tileset.get_tile(tile_index)
#                     self.screen.blit(tile, (x, y, *self.size))
#                 x += self.size[0]
#             x = x0
#             y += self.size[1]

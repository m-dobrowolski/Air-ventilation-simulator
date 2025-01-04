class Settings:
    def __init__(self):
        # Screen settings
        self.tiles_num_border = 20
        self.screen_width, self.screen_height = self.tiles_num_border * 32, self.tiles_num_border * 32
        # Tiles settings
        self.tileset_file = "/level_editor/images/tileset.png"
        self.tileset_margin = 1
        self.tileset_spacing = 1
        self.tile_size = (32, 32)  # width, height

from custom_animation import SpriteSheetAnimation

sprite_data = {'player':{'shoot': ((26, 0), (27, 0)),'run': ((15, 0), (25, 0)),
                         'jump': ((9, 0), (14, 0)),'idle': ((5, 0), (8, 0)),
                         'die': ((0, 0), (3, 0)),}
                         
                         }


class CharectorAnime:
    def __init__(self, target):
        self.target = target

    def player_anime(self):    
        player_graphics = SpriteSheetAnimation('resorces/charecters/combined_image', tileset_size=(27, 1), fps=6, animations=sprite_data['player'],position=self.target.position, scale=(35, 35, 1))
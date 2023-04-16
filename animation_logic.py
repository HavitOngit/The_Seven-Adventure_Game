from custom_animation import SpriteSheetAnimation
from ursina import held_keys
sprite_data = {'player':{'shoot': ((26, 0), (27, 0)),'run': ((15, 0), (25, 0)),
                         'jump': ((9, 0), (14, 0)),'idle': ((5, 0), (8, 0)),
                         'die': ((0, 0), (3, 0)),}
                         
                         }


class CharectorAnimator:
    def __init__(self, target):
        self.target = target
        
    def player_anime(self):    
        player_anim = SpriteSheetAnimation('resorces/charecters/combined_image', tileset_size=(27, 1), fps=6, animations=sprite_data['player'],position=self.target.position, scale=(35, 35, 1))

    def controls(self, player_anim):
        def input(key):
            if key == 'd':
                player_anim.play_animation('run')
            elif key == 'space':
                player_anim.play_animation('jump')
            elif key == 'f':
                player_anim.play_animation('shoot')
              
    def improv_anim(self, player_anim):
        if not held_keys['d']:
            player_anim.play_animation('idle')

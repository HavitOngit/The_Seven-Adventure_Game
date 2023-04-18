from ursina import *
import math



class Enemy:
    def __init__(self, sprite_path, animations_data, position, scale, reference, tileset):
        self.sprite_path = sprite_path
        self.animations_data = animations_data
        self.position = position
        self.scale = scale
        self.reference = reference
        self.tileset = tileset
        self.animation = SpriteSheetAnimation(self.sprite_path, tileset_size=tileset, fps=9, animations=self.animations_data,position=self.position, scale=self.scale)

    def run_towards_player(self, player_reference, speed):
        player_position = player_reference.position
        enemy_position = self.position
        
        # Calculate the angle between the enemy and the player
        dx = player_position[0] - enemy_position[0]
        dy = player_position[1] - enemy_position[1]
        angle = math.atan2(dy, dx)
        
        # Calculate the enemy's new position based on its speed and the angle to the player
        new_x = enemy_position[0] + speed * math.cos(angle)
        new_y = enemy_position[1] + speed * math.sin(angle)
        
        # Update the enemy's position
        self.position = (new_x, new_y)

def brainer(player):
    data = {'path':'resorces\charecters\\briner.png', 'tileset':(8, 6)}
    brainer = Enemy(sprite_path=data['path'], animations_data={'run': ((0, 5), (3, 5))}, tileset=data['tileset'], scale=(35, 35, 1), position=player.position, reference=player)
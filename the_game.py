from ursina import *
from ursina.prefabs.health_bar import HealthBar

from time import sleep

from custom_animation import SpriteSheetAnimation

app = Ursina()

from ursina.prefabs.platformer_controller_2d import PlatformerController2d


# t=time.time()
player = PlatformerController2d(
    walk_speed=100,
    x=50,
    y=650,
    z=0.01,
    scale_x=25,
    scale_y=25,
    max_jumps=8,
    jump_duration=0.3,
    jump_height=30,
    color=(123, 214, 123, .10)
)
a = Entity(model='cube', texture='resorces\collectables\Medkit.png', collider = 'box', scale = (95, 53, 1), position = (405, 217, 0.01))
### Animation
player_graphics = SpriteSheetAnimation('resorces/charecters/combined_imager+l', tileset_size=(27, 2), fps=9,position=player.position, scale=(35, 35, 1), animations={
    'shoot': ((25, 0), (26, 0)),
    'run': ((15, 0), (24, 0)),
    'jump': ((9, 0), (14, 0)),
    'idle': ((5, 0), (8, 0)),
    'die': ((0, 0), (3, 0)),


    'left_run':((2, 1), (11, 1)),
    'left_idle': ((19, 1), (22, 1)),
    'left_jump': ((12, 1), (18, 1)),
    'left_shoot': ((0, 1), (1, 1)),

})

### enemy
enime_graphics = SpriteSheetAnimation('resorces\charecters\\briner.png', tileset_size=(8, 6), fps=9,position=player.position, scale=(35, 35, 1), animations={
    'hyper': ((0, 3), (5, 3)),
    'run': ((0, 5), (3, 5)),
    
})




def enime_attack():
    dife = player.x - enime_graphics.x
    if dife <= 5:
        enime_graphics.play_animation('hyper')
    if enime_graphics.position <= (564, 356, -2):
        enime_graphics.x += 2
    if enime_graphics.position <= (362, 356, -2):
        enime_graphics.x -= 2    
           


### Enime end
### animation End
window = WindowPanel(
    title="GAME OVER!!",
    # content="This is a pop-up window!",
    scale=(0.9, 0.6),
    draggable=False,
    visible=False,
    #texture="Game_Over_Msg.jpg",
)
player1 = WindowPanel(
    title="Player",
    roundness=1,
    window_color=color.red,
    scale=(0.6, 0.04),
    position=(-0.85, 0.5),
)

HB1 = HealthBar(
    bar_color=color.lime.tint(-0.25),
    roundness=0.5,
    color=color.red,
    scale=(1.2, 0.04),
    position=(-0.8, 0.5),
)


def acid():
    distance = Vec2(player.x, player.y) - Vec2(1688, 201)
    dis = Vec2(player.x, player.y) - Vec2(571, 129)
    if distance.length() < 30:
        damage(5)
    if dis.length() < 20:
        damage(5)

def damage(power):
    HB1.value -= power

# invoke(damage, delay=1, repeat=True)


def heal(power):
    HB1.value += power

def health():
    
    if a.intersects(player):
        heal(50)
    
    
ground = Entity(model="quad", scale_x=10, collider="box", color=color.black)
restart_button = Button(
    text="Restart", scale=(0.1, 0.05), position=(0, -0.1), visible=False
)

quad = load_model("quad", use_deepcopy=True)

level_parent = Entity(
    model=Mesh(vertices=[], uvs=[]), texture="white_cube", color=(244, 244, 244, 0)
)
bg = Entity(
    model="quad",
    position=(962, 545, 1),
    scale=(1950, 1080),
    texture="resorces/Background/Level_1_final.png",
)


def make_level(texture):
    [destroy(c) for c in level_parent.children]
    pos = []
    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x, y)

            if col == color.black:
                level_parent.model.vertices += [
                    Vec3(*e) + Vec3(x + 0.5, y + 0.5, 0)
                    for e in quad.generated_vertices
                ]
                level_parent.model.uvs += quad.uvs

                if not collider:
                    collider = Entity(
                        parent=level_parent,
                        position=(x, y),
                        model="quad",
                        origin=(-0.5, -0.5),
                        collider="box",
                        visible=False,
                    )
                else:
                    collider.scale_x += 1
                    pos.append(collider.position)
            else:
                collider = None

    level_parent.model.generate()


make_level(load_texture("resorces/Levels/level_1_collider_f"))

camera.orthographic = True
camera.position = (0, 0)
camera.fov = 800


camera.add_script(SmoothFollow(target=player, offset=[0, 5, -30], speed=4))
player.traverse_target = level_parent
enemy = Entity(model="cube", collider="box", color=color.red, position=(16, 5, -0.1))

# for player animation

isfacingR = 1
mover = 1
def update():
    global mover
    
    ### animation alingment
    player_graphics.position = player.position
    player_graphics.x = player.x + 10
    player_graphics.y = player.y + 20
    # player_graphics.z = -1

    if isfacingR == -1:
        player_graphics.x = player.x - 10    

    ###
    # player.x += isfacingR

    acid()
    health()

    ### Enime
    enime_attack()

    if player.intersects(enemy).hit:
        print("die")
        
        

    if HB1.value == 0:
        print("GAME OVER!!!")
        

        
    if player.y < 0:
        HB1.value = 0
        window.visible = True
        restart_button.visible = True
        
        

    if held_keys["shift"]:
        player.walk_speed = 300
    else:
        player.walk_speed = 100


    is_idle = held_keys['d'] + held_keys['a'] + held_keys['space'] + held_keys['f']
    if is_idle == 0:
        if isfacingR == 1:
            print(isfacingR)
            player_graphics.play_animation('idle')
        else:
            print(isfacingR)
            player_graphics.play_animation('left_idle')    
    
# trial for animation
#enime_graphics.play_animation('run')

def input(key):
    global isfacingR

    if key == 'd':
        isfacingR = 1
        player_graphics.play_animation('run')
          
    if key == 'a':
        isfacingR = -1
        player_graphics.play_animation('left_run')
           
    if key == 'space':
        print(isfacingR)
        if isfacingR == 1:
            player_graphics.play_animation('jump')
        else:
            player_graphics.play_animation('left_jump')

    if key == 'f':
        if isfacingR == 1:
            player_graphics.play_animation('shoot')
        else:
            player_graphics.play_animation('left_shoot')

# only for bg       
  
Sky(color=color.dark_gray)
#####

input_handler.bind("right arrow", "d")
input_handler.bind("left arrow", "a")
input_handler.bind("up arrow", "space")
input_handler.bind("down arrow", "b")
input_handler.bind("gamepad dpad right", "d")
input_handler.bind("gamepad dpad left", "a")
input_handler.bind("gamepad a", "space")

EditorCamera()
app.run()
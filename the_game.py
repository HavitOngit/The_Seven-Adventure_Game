from ursina import *
import pyautogui
from time import sleep
from massage_ui import Show_massage
from animation_logic import CharectorAnimator
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()



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

### Animation
player_animation = CharectorAnimator(player)

### animation End
Show_massage()


def acid():
    distance = Vec2(player.x, player.y) - Vec2(1688, 201)
    dis = Vec2(player.x, player.y) - Vec2(571, 129)
    if distance.length() < 30:
        damage(5)
    if dis.length() < 80:
        damage(5)

def damage():
    HB1.value -= 1

# invoke(damage, delay=1, repeat=True)


def heal(power):
    HB1.value += power


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


def update():
    ### animation alingment
    player_animation.position = player.position
    player_animation.x = player.x + 10
    player_animation.y = player.y + 20
    ###

    acid()
    if player.intersects(enemy).hit:
        print("die")
        sleep(1)
        pyautogui.click(x=1687, y=111)

    if HB1.value == 0:
        print("GAME OVER!!!")
        sleep(1)
        pyautogui.click(x=1687, y=111)
        return 0
    if player.y < 0:
        HB1.value = 0
        window.visible = True
        restart_button.visible = True
        sleep(1)
        pyautogui.click(x=1687, y=111)

    if held_keys["shift"]:
        player.walk_speed = 300
    else:
        player.walk_speed = 100

    if not held_keys['d']:
        player_animation.play_animation('idle')




# trial for animation
def input(key):
    if key == 'd':
        print('runing...')
        player_animation.play_animation('run')
    elif key == 'space':
        print('runing...')
        player_animation.play_animation('jump')
    elif key == 'f':
        print('runing...')
        player_animation.play_animation('shoot')


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

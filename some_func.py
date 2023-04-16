from ursina import input_handler
def ArrowKeys():
    input_handler.bind("right arrow", "d")
    input_handler.bind("left arrow", "a")
    input_handler.bind("up arrow", "space")
    input_handler.bind("down arrow", "b")
    input_handler.bind("gamepad dpad right", "d")
    input_handler.bind("gamepad dpad left", "a")
    input_handler.bind("gamepad a", "space")

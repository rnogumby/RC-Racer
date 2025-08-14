from ursina import *

app = Ursina()

# Start screen
start_screen = Entity(parent=camera.ui, model='quad', scale=(1.5,0.5), color=color.black, position=(0,0,0), texture=None)
start_text = Text(text='RC Racer 3D\nPress SPACE to start', origin=(0,0), scale=2, parent=start_screen, position=(0,0,0.1))

car = None
track = None
started = False
speed = 0
turn_speed = 90

def start_game():
    global car, track, started
    start_screen.enabled = False
    start_text.enabled = False
    # Create track and car
    track = Entity(model='plane', scale=(20,1,20), color=color.gray, texture='white_cube', texture_scale=(20,20), position=(0,0,0))
    car = Entity(model='cube', color=color.red, scale=(1,0.5,2), position=(0,0.5,0))
    camera.position = (0, 15, -25)
    camera.look_at(car)
    started = True

def update():
    global speed
    if not started:
        if held_keys['space']:
            start_game()
        return
    # Car controls
    if held_keys['w']:
        speed += 0.1
    if held_keys['s']:
        speed -= 0.1
    speed *= 0.95
    if held_keys['a']:
        car.rotation_y += turn_speed * time.dt
    if held_keys['d']:
        car.rotation_y -= turn_speed * time.dt
    car.position += car.forward * speed * time.dt

app.run()

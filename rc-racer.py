import pygame, math, random

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load car sprite


# ...existing code...
car_image = pygame.image.load("RC-Racer/nissan-skyline-gt-r.png").convert_alpha()
# ...existing code...
# Track parameters (scaled to screen)
TRACK_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
TRACK_RX = int(SCREEN_WIDTH * 0.35)
TRACK_RY = int(SCREEN_HEIGHT * 0.3)
TRACK_WIDTH = max(40, int(min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.08))
START_LINE_X = TRACK_CENTER[0]
START_LINE_Y1 = TRACK_CENTER[1] - TRACK_RY
START_LINE_Y2 = TRACK_CENTER[1] + TRACK_RY

# Scale car to fit track width
CAR_SIZE = int(TRACK_WIDTH * 0.8)
car = pygame.transform.smoothscale(car_image, (CAR_SIZE, CAR_SIZE))
# Start car at the start/finish line, facing up the track
car_x = START_LINE_X
car_y = START_LINE_Y2 - CAR_SIZE // 2
angle = 0  # 0 degrees = facing up
speed = 0

# Start screen
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)
show_start = True
while show_start:
    screen.fill((30, 30, 30))
    title = font.render("RC Racer", True, (200, 200, 200))
    instr = small_font.render("Press SPACE to start. Use arrow keys to drive.", True, (200, 200, 200))
    screen.blit(title, (250, 200))
    screen.blit(instr, (170, 300))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            show_start = False


# Track parameters (scaled to screen)
TRACK_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
TRACK_RX = int(SCREEN_WIDTH * 0.35)
TRACK_RY = int(SCREEN_HEIGHT * 0.3)
TRACK_WIDTH = max(40, int(min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.08))
START_LINE_X = TRACK_CENTER[0]
START_LINE_Y1 = TRACK_CENTER[1] - TRACK_RY
START_LINE_Y2 = TRACK_CENTER[1] + TRACK_RY

# Lap counting
lap_count = 0
passed_start = False
NUM_OPPONENTS = 3
opponents = []
for i in range(NUM_OPPONENTS):
    opp_x = random.randint(TRACK_CENTER[0] - TRACK_RX + TRACK_WIDTH, TRACK_CENTER[0] + TRACK_RX - TRACK_WIDTH)
    opp_y = random.randint(TRACK_CENTER[1] - TRACK_RY + TRACK_WIDTH, TRACK_CENTER[1] + TRACK_RY - TRACK_WIDTH)
    opp_angle = random.randint(0, 360)
    opp_speed = random.uniform(2, 4)
    opponents.append({"x": opp_x, "y": opp_y, "angle": opp_angle, "speed": opp_speed})

def inside_track(x, y):
    dx = x - TRACK_CENTER[0]
    dy = y - TRACK_CENTER[1]
    dist = ((dx / TRACK_RX) ** 2 + (dy / TRACK_RY) ** 2) ** 0.5
    return dist < 1 and dist > ((TRACK_RX - TRACK_WIDTH) / TRACK_RX)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()


    # Car controls: UP/DOWN for forward/backward, LEFT/RIGHT for turning
    if keys[pygame.K_UP]:
        speed += 0.2
    if keys[pygame.K_DOWN]:
        speed -= 0.2
    if keys[pygame.K_LEFT]:
        angle += 4
    if keys[pygame.K_RIGHT]:
        angle -= 4

    speed *= 0.95  # friction

    # Move car in direction it is facing (0 degrees = up)
    rad = math.radians(angle)
    next_x = car_x + math.sin(rad) * speed
    next_y = car_y - math.cos(rad) * speed
    if inside_track(next_x, next_y):
        car_x, car_y = next_x, next_y
    else:
        speed *= 0.5  # slow down if off track

    # Lap counting (crossing start line from bottom to top)
    if car_y < TRACK_CENTER[1] and not passed_start and abs(car_x - START_LINE_X) < 20:
        lap_count += 1
        passed_start = True
    if car_y > TRACK_CENTER[1]:
        passed_start = False

    # Update opponent cars
    for opp in opponents:
        opp_next_x = opp["x"] + math.sin(math.radians(opp["angle"])) * opp["speed"]
        opp_next_y = opp["y"] + math.cos(math.radians(opp["angle"])) * opp["speed"]
        if inside_track(opp_next_x, opp_next_y):
            opp["x"] = opp_next_x
            opp["y"] = opp_next_y
        else:
            opp["angle"] += random.choice([-90, 90])  # turn if off track
        if random.random() < 0.02:
            opp["angle"] += random.choice([-5, 5])


    screen.fill((20, 80, 20))  # green background for grass
    # Draw track (outer and inner ovals)
    pygame.draw.ellipse(screen, (120, 120, 120), (TRACK_CENTER[0]-TRACK_RX, TRACK_CENTER[1]-TRACK_RY, TRACK_RX*2, TRACK_RY*2), 0)
    pygame.draw.ellipse(screen, (20, 80, 20), (TRACK_CENTER[0]-(TRACK_RX-TRACK_WIDTH), TRACK_CENTER[1]-(TRACK_RY-TRACK_WIDTH), (TRACK_RX-TRACK_WIDTH)*2, (TRACK_RY-TRACK_WIDTH)*2), 0)
    # Draw start/finish line
    pygame.draw.line(screen, (255,255,255), (START_LINE_X, START_LINE_Y1), (START_LINE_X, START_LINE_Y2), 4)
    # Draw opponents
    for opp in opponents:
        opp_car = pygame.transform.rotate(car, opp["angle"])
        opp_rect = opp_car.get_rect(center=(opp["x"], opp["y"]))
        screen.blit(opp_car, opp_rect)
    # Draw player car
    rotated_car = pygame.transform.rotate(car, angle)
    rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rect)
    # Draw lap counter
    lap_text = small_font.render(f"Lap: {lap_count}", True, (255,255,0))
    screen.blit(lap_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

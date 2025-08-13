import pygame, math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load car sprite
car_image = pygame.image.load("RC-Racer/nissan-skyline-gt-r.png").convert_alpha()
car = car_image
car_x, car_y = 400, 300
angle = 0
speed = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speed += 0.2
    if keys[pygame.K_DOWN]:
        speed -= 0.2
    if keys[pygame.K_LEFT]:
        angle += 4
    if keys[pygame.K_RIGHT]:
        angle -= 4

    speed *= 0.95  # friction

    car_x += math.sin(math.radians(angle)) * speed
    car_y += math.cos(math.radians(angle)) * speed

    screen.fill((30, 30, 30))
    rotated_car = pygame.transform.rotate(car, angle)
    rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

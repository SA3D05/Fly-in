import pygame
import sys

pygame.init()
pygame.mouse.set_visible(False)

window = pygame.display.set_mode((1920, 1080))

cursor = pygame.image.load("assets/cursor.png").convert()
clock = pygame.time.Clock()
cursor = pygame.transform.scale(cursor, (30, 30))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.fill("black")
    x,y = pygame.mouse.get_pos()
    window.blit(cursor,(x , y ))
    pygame.display.update()
    clock.tick(60)
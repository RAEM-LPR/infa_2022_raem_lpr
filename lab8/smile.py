import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

screen.fill((127,127,127))

circle(screen, (0, 0, 0), (200, 175), 154)
circle(screen, (255, 255, 0), (200, 175), 150)
circle(screen, (0, 0, 0), (260, 130), 22)
circle(screen, (0, 0, 0), (140, 130), 22)
circle(screen, (255, 0, 0), (260, 130), 20)
circle(screen, (255, 0, 0), (140, 130), 20)
circle(screen, (0, 0, 0), (260, 130), 10)
circle(screen, (0, 0, 0), (140, 130), 10)
line(screen,  (0, 0, 0), (140, 270), (260, 270), 30)
line(screen,  (0, 0, 0), (40, 40), (180, 130), 15)
line(screen,  (0, 0, 0), (350, 60), (220, 120), 15)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
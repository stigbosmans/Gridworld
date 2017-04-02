import numpy as np
import pygame
from World import World, BasicWorld, RandomPlayerWorld, RandomWorld, WorldVisualizer
(width, height) = (205, 205)

def keyHandler(key):
    action=0
    if event.key==pygame.K_LEFT:
        action=2
    elif event.key==pygame.K_RIGHT:
        action=3
    elif event.key==pygame.K_UP:
        action=0
    elif event.key==pygame.K_DOWN:
        action=1
    return action

pygame.init()
screen = pygame.display.set_mode((width, height))

wereld=RandomPlayerWorld()
wereld.showWorld()
visualizer=WorldVisualizer(wereld,screen)

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            print(keyHandler(event.key))
            visualizer.update()

import pygame
from pygame.locals import *
import sys
from FABRIK import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

points = [(SCREEN_WIDTH/2, SCREEN_HEIGHT * 1),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.75),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.5),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.25)]

body = Body(points)

def DrawBody(body: Body, screen):
    for joint in body.joints:
        #print(joint.x, joint.y)
        pygame.draw.circle(screen, BLACK, pygame.Vector2(joint.x, joint.y), 5)

    for conn in body.connections:
        startPos = pygame.Vector2(body.joints[conn.a].x, body.joints[conn.a].y)
        endPos = pygame.Vector2(body.joints[conn.b].x, body.joints[conn.b].y)
        pygame.draw.line(screen, BLACK, startPos, endPos)

        
def main():
    running = True
    while running:     
        for event in pygame.event.get():              
            if event.type == QUIT:
                running = False
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                body.reach(x, y)

            DISPLAYSURF.fill(WHITE)
            DrawBody(body, DISPLAYSURF)
            
            pygame.display.flip()
            FramePerSec.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

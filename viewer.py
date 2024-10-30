import pygame
from pygame.locals import *
import sys
from FABRIK import *
import time
import numpy as np
from scipy.special import comb


def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)

    result = 0
    for n in range(0, N + 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result

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
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900
 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

points = [(SCREEN_WIDTH/2, SCREEN_HEIGHT * 1),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.9),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.8),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.5),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.3),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.1)]

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
    prev_x, prev_y = 0, 0
    while running:     
        for event in pygame.event.get():              
            if event.type == QUIT:
                running = False
                continue
            # elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            #     x, y = pygame.mouse.get_pos()
            #     body.reach(x, y, tol = 10)
            #     print(x, y)
            #     continue

            #     t = 200
            #     start_x = body.joints[-1].x
            #     start_y = body.joints[-1].y
            #     start_time = time.time()
            #     end_time = t
            #     current_time = 0
                
            #     while current_time < end_time:
            #         current_time += time.time() - start_time
            #         current_time = current_time if current_time < end_time else end_time
            #         l = current_time / end_time
            #         ls = smoothstep(l, 0, 1, N=2)
            #         print(l, ls)
            #         #print(l, ls)
            #         xi = ls * (x - start_x) + start_x
            #         yi = ls * (y - start_y) + start_y
            #         #print(xi, yi)
            #         body.reach(int(xi), int(yi), tol=10)
            #         DISPLAYSURF.fill(WHITE)
            #         pygame.draw.circle(DISPLAYSURF, GREEN, pygame.Vector2(x, y), 5)
            #         DrawBody(body, DISPLAYSURF)
            #         pygame.display.flip()
            #         self.reach(x, y)
        |
        |
        
        DISPLAYSURF.fill(WHITE)
        x, y = pygame.mouse.get_pos()
        if x != prev_x and y != prev_y:
            body.reach(x, y, tol = 1)
            prev_x = x
            prev_y = y
        pygame.draw.circle(DISPLAYSURF, GREEN, pygame.Vector2(x, y), 10)
        DrawBody(body, DISPLAYSURF)
            
        pygame.display.flip()
        FramePerSec.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

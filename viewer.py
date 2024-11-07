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
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.95),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.9),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.85),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.8),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.75),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.7),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.65),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.6),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.55),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.5),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.45),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.4),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.35),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.3),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.25),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.15),
          (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.1)]

body = Body(points)


def DrawBody(body: Body, screen):
    for joint in body.joints:
        pygame.draw.circle(screen, BLACK, pygame.Vector2(joint.x, joint.y), 5)

    for conn in body.connections:
        startPos = pygame.Vector2(body.joints[conn.a].x, body.joints[conn.a].y)
        endPos = pygame.Vector2(body.joints[conn.b].x, body.joints[conn.b].y)
        pygame.draw.line(screen, BLACK, startPos, endPos)

        
def main():    
    running = True
    follow_mouse = False
    edit_mode = False
    prev_x, prev_y = 0, 0
    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    mouse_follow_t = font.render('E = mouse following', True, (0, 0, 0))
    trim_arm_t = font.render('T = trim arm', True, (0, 0, 0))
    clear_all_t = font.render('C = clear all', True, (0, 0, 0))
    new_joint_t = font.render('Left Click = new joint', True, (0, 0, 0))

    while running:     
        for event in pygame.event.get():              
            if event.type == QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    follow_mouse = not follow_mouse

                if event.key == pygame.K_t:
                    body.delete_last()

                if event.key == pygame.K_c:
                    body.clear_all()


            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                body.add_joint(x, y)
            
            # IF FOLLOW_MOUSE IS NOT ACTIVATED
            elif not follow_mouse and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:    
                x, y = pygame.mouse.get_pos()
                
                t = 200
                start_x = body.joints[-1].x
                start_y = body.joints[-1].y
                start_time = time.time()
                end_time = t
                current_time = 0
                
                while current_time < end_time:
                    current_time += time.time() - start_time
                    current_time = current_time if current_time < end_time else end_time
                    l = current_time / end_time
                    ls = smoothstep(l, 0, 1, N=3)
                    
                    xi = ls * (x - start_x) + start_x
                    yi = ls * (y - start_y) + start_y
                    
                    body.reach(int(xi), int(yi), tol=3)
                    DISPLAYSURF.fill(WHITE)
                    DISPLAYSURF.blit(mouse_follow_t, dest=(0,0))
                    DISPLAYSURF.blit(trim_arm_t, dest=(0,15))
                    DISPLAYSURF.blit(clear_all_t, dest=(0,30))
                    DISPLAYSURF.blit(new_joint_t, dest=(0,45))
                    pygame.draw.circle(DISPLAYSURF, RED, pygame.Vector2(x, y), 10)
                    DrawBody(body, DISPLAYSURF)
                    pygame.display.flip()

                    
        DISPLAYSURF.fill(WHITE)
        # DISPLAY TEXT
        DISPLAYSURF.blit(mouse_follow_t, dest=(0,0))
        DISPLAYSURF.blit(trim_arm_t, dest=(0,15))
        DISPLAYSURF.blit(clear_all_t, dest=(0,30))
        DISPLAYSURF.blit(new_joint_t, dest=(0,45))
        
        # FOLLOW MOUSE ALL THE TIME
        x, y = pygame.mouse.get_pos()
        if follow_mouse and x != prev_x and y != prev_y:
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

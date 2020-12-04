import pygame, random
from pygame.locals import *
from pygame import Vector3

from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:
    def __init__(self, pos, size):

        self.pos = pos
        self.x, self.y, self.z = self.pos[0], self.pos[1], self.pos[2]

        self.size = size
        self.l, self.w, self.h = self.size[0], self.size[1], self.size[2]

        self.vertices = [
            ( (self.x + (self.w/2)), (self.y - (self.h/2)), (self.z - (self.l/2)) ), 
            ( (self.x + (self.w/2)), (self.y + (self.h/2)), (self.z - (self.l/2)) ), 
            ( (self.x - (self.w/2)), (self.y + (self.h/2)), (self.z - (self.l/2)) ), 
            ( (self.x - (self.w/2)), (self.y - (self.h/2)), (self.z - (self.l/2)) ), 
            ( (self.x + (self.w/2)), (self.y - (self.h/2)), (self.z + (self.l/2)) ), 
            ( (self.x + (self.w/2)), (self.y + (self.h/2)), (self.z + (self.l/2)) ), 
            ( (self.x - (self.w/2)), (self.y - (self.h/2)), (self.z + (self.l/2)) ), 
            ( (self.x - (self.w/2)), (self.y + (self.h/2)), (self.z + (self.l/2)) ), 
        ]
        self.edges = [
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        ]

    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

class FPPCamera:
    def __init__(self, pos, WW, WH):
        gluPerspective(50, (WW / WH), 0.1, 50)
        glTranslatef(pos[0], pos[1], pos[2])
        glRotatef(0, 0, 0, 0)

        self.pos = Vector3(pos)

        self.rot = Vector3(0, 0, 0)
        self.rot_angle = 0

        self.velocity = Vector3(0, 0, 0)
        self.rot_velocity = Vector3(0, 0, 0)
    
    def update(self):
        # self.pos += self.velocity

        # self.rot += self.rot_velocity

        if self.velocity.x != 0:
            self.pos.x += self.velocity.x
        if self.velocity.y != 0:
            self.pos.y += self.velocity.y
        if self.velocity.z != 0:
            self.pos.z += self.velocity.z
        
        if self.rot_velocity.x != 0:
            self.rot.x += self.rot_velocity.x
        if self.rot_velocity.y != 0:
            self.rot.y += self.rot_velocity.y
        if self.rot_velocity.z != 0:
            self.rot.z += self.rot_velocity.z

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        glRotatef(self.rot_angle, self.rot.x, self.rot.y, self.rot.z)

def main():
    WW = 800
    WH = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WW, WH), DOUBLEBUF | OPENGL)

    ## Objects
    cubes = []
    for i in range(10):
        pos = (random.randint(-5, 5), 0, -5)
        size = (random.randint(1, 5), random.randint(1, 5), random.randint(1, 5))
        c = Cube(pos, size)
        cubes.append(c)

    cam = FPPCamera((0, 0, 0), WW, WH)
    player_vel = 0.1

    ## Quadrants
    quadrant = [
        (range(WW//2, WW), range(0, WH)), 
        (range(0, WW//2), range(0, WH))
    ]

    running = True
    clicked = False
    while running:
        mx, my = pygame.mouse.get_pos()
        # clock.tick(120)
        cam.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cam.velocity.z = player_vel
                if event.key == pygame.K_DOWN:
                    cam.velocity.z = -player_vel
                if event.key == pygame.K_RIGHT:
                    cam.velocity.x = -player_vel
                if event.key == pygame.K_LEFT:
                    cam.velocity.x = player_vel

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    cam.velocity.z = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    cam.velocity.x = 0
        
        for cube in cubes:
            cube.draw()
        
        # cam
        # if clicked:
        #     if mx in quadrant[0][0] and my in quadrant[0][1]:
        #         cam.rotate(1, 0, 1, 0)
        #     if mx in quadrant[1][0] and my in quadrant[1][1]:
        #         cam.rotate(1, 0, -1, 0)

        pygame.display.flip()
        pygame.time.wait(10)


main()

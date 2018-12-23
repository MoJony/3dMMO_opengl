import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import random

from gl_camera import FirstPersonCamera
#  ----------------------------
#  stuff for openGL

MOUSE_SENSEITIVITY = 0.1

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

colors = (  # R,G,B
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

ground_surfaces = (0,1,2,3)

ground_vertices = (
    (-10,-0.1,50),
    (10,-0.1,50),
    (-10,-0.1,-300),
    (10,-0.1,-300),

    )


#  -------------

# def goto(x, y, z, pitch, yaw, roll):
#     glMatrixMode(GL_MODELVIEW)
#
#     glLoadIdentity()
#     glRotatef(pitch,1,0,0)
#     glRotatef(yaw,0,1,0)
#     glRotatef(roll,0,0,1)
#     glTranslatef(-x,-y,-z)


def ground():

    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 0))  # green
        glVertex3fv(vertex)

    glEnd()


def cube():
    # creating the cubes
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            g = vertices[vertex]
            glVertex3fv(vertices[vertex])
    glEnd()
    # coloring
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(colors[0])  # can use other colors in the colors list sticking to red for now
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    tx = 0  # ffff
    ty = 0
    tz = 0
    ry = 0
    rx = 0
    so_broken = 0
    so_broken_sum = 0

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    def IdentityMat44():
        return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')

    view_mat = IdentityMat44()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()



    #glRotatef(0, 0, 1, 0)
    #glRotatef(0, 1, 0, 0)

    #cam = FirstPersonCamera()
    #input_handler = cam.InputHandler()

    mousepos = pygame.mouse.get_pos()
    new_mouse_pos = pygame.mouse.get_pos()

    while True:  # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_a:
                    tx = 0.1
                elif event.key == pygame.K_d:
                    tx = -0.1
                elif event.key == pygame.K_w:
                    tz = 0.1
                elif event.key == pygame.K_s:
                    tz = -0.1
                elif event.key == pygame.K_LEFT:
                    so_broken = -0.1 + so_broken
                elif event.key == pygame.K_RIGHT:
                    so_broken = 0.1 + so_broken
                # elif event.key == pygame.K_RIGHT:
                #     ry = 1.0
                # elif event.key == pygame.K_LEFT:
                #     ry = -1.0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and tx > 0:
                    tx = 0
                elif event.key == pygame.K_d and tx < 0:
                    tx = 0
                elif event.key == pygame.K_w and tz > 0:
                    tz = 0
                elif event.key == pygame.K_s and tz < 0:
                    tz = 0
                elif event.key == pygame.K_LEFT:
                    so_broken = 0
                elif event.key == pygame.K_RIGHT:
                    so_broken = 0
                # elif event.key == pygame.K_RIGHT and ry > 0:
                #     ry = 0.0
                # elif event.key == pygame.K_LEFT and ry < 0:
                #     ry = 0.0

            if event.type == pygame.MOUSEMOTION:
                mousepos = new_mouse_pos
                #mousepos = pygame.mouse.get_rel()
                new_mouse_pos = pygame.mouse.get_pos()
                ry = new_mouse_pos[0] - mousepos[0]
                ry = ry * -1
                rx = new_mouse_pos[1] - mousepos[1]
                rx = rx * -1
                pygame.mouse.set_pos(400, 300)
                mousepos = (400,300)
                pygame.mouse.get_rel()
                print(ry)
                #print(mousepos, ' / ', new_mouse_pos)   # mojo
                #input_handler.on_mouse_motion(mousepos[0],mousepos[1],new_mouse_pos[0],new_mouse_pos[1])

                #glRotatef(25,new_mouse_pos[0], new_mouse_pos[1], 0)  # Mojo broken as fuckkkkk !!!


            '''
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 4:
                                glTranslatef(0,0,1.0)

                            if event.button == 5:
                                glTranslatef(0,0,-1.0)
            '''

        # x = glGetDoublev(GL_MODELVIEW_MATRIX)
        # camera_x = x[3][0]
        # camera_y = x[3][1]
        # camera_z = x[3][2]
        # #glRotatef(1, 0, 2, 0)
        # #glRotatef(2, 0, 1, 0)
        # glTranslatef(x_move, y_move, 0)
        #glRotate(1, 0, 2, 0)

        glPushMatrix()
        glLoadIdentity()

        glTranslatef(tx, ty, tz)


        glRotatef(rx * MOUSE_SENSEITIVITY, 1, 0, 0)

        glRotatef(ry * MOUSE_SENSEITIVITY, 0, 1, 0)


        so_broken_sum = so_broken_sum + so_broken  # mojo MoJo broken
        print(so_broken_sum)
        #glRotatef(so_broken, 0, 0, 1)


        ry = 0
        glMultMatrixf(view_mat)

        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        ground()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

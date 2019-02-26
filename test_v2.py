import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *



vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1, ),
    (-1, -1, 1),
    (-1, 1, 1),
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
    (5,7),
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6),
    )

colors = (
    (1,1,1),
    (0,0,0),
    (0,1,1),
    (0,0,0),
    (0,1,1),
    (1,0,1),
    (0,0,0),
    (1,1,1),
    (0,0,0),
    (0,1,1),
    )

def Cube():
    glBegin(GL_QUADS)


    for surface in surfaces:
        x = 0

        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])


    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()


def main():
    tx = 0
    ty = 0
    tz = 0
    ry = 0

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    view_mat = IdentityMat44()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()

    while True:

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
                elif event.key == pygame.K_RIGHT:
                    ry = 1.0
                elif event.key == pygame.K_LEFT:
                    ry = -1.0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and tx > 0:
                    tx = 0
                elif event.key == pygame.K_d and tx < 0:
                    tx = 0
                elif event.key == pygame.K_w and tz > 0:
                    tz = 0
                elif event.key == pygame.K_s and tz < 0:
                    tz = 0
                elif event.key == pygame.K_RIGHT and ry > 0:
                    ry = 0.0
                elif event.key == pygame.K_LEFT and ry < 0:
                    ry = 0.0

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(tx, ty, tz)
        glRotatef(ry, 0, 1, 0)
        glMultMatrixf(view_mat)

        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)
main()
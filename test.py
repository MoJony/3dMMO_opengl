import pygame
from pygame.locals import *

import glm
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import transformations
from transformations import quaternion_matrix
from transformations import quaternion_matrix

import pyquaternion
#from pyquaternion import Quaternion

import random
from math import *
import math
#from ZMath import *

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

def camera():
    pass
    pitch = Quaternion(radians(self.pitchAngle), glm.vec3(1, 0, 0))
    yaw = Quaternion(radians(self.yawAngle), glm.vec3(0, 1, 0))
    roll = Quaternion(radians(self.rollAngle), glm.vec3(0, 0, 1))

    quat = pitch * yaw * roll

    # glRotated(degrees(quat.x), 1.0, 0.0, 0.0);
    # glRotated(degrees(quat.y), 0.0, 1.0, 0.0);
    # glRotated(degrees(quat.z), 0.0, 0.0, 1.0);

    viewMatrix = quat.toMatrix()
    glMultMatrixf(viewMatrix)

    quat = yaw * pitch * roll
    mat = quat.toMatrix()

    strafeVector.x = mat[0][0]
    strafeVector.y = mat[0][1]
    strafeVector.z = mat[0][2]

    forwardVector.x = mat[2][0]
    forwardVector.y = mat[2][1]
    forwardVector.z = mat[2][2]

    # self.upVector.x = mat[1][0]
    # self.upVector.y = mat[1][1]
    # self.upVector.z = mat[1][2]
    upVector.y = 1

    strafeVector *= self.strafe
    forwardVector *= self.forward
    upVector *= self.up

    position += forwardVector + strafeVector + upVector
    # self.position.z = -self.position.z

    glTranslatef(-position.x, -position.y, position.z)


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

        # pitch = Quaternion(radians(rx * MOUSE_SENSEITIVITY), glm.vec3(1, 0, 0))
        # yaw = Quaternion(radians(ry * MOUSE_SENSEITIVITY), glm.vec3(0, 1, 0))
        # roll = Quaternion(0, glm.vec3(0, 0, 1))

        # pitch = glm.quat(radians(rx * MOUSE_SENSEITIVITY), glm.vec3(1, 0, 0))
        # yaw = glm.quat(radians(ry * MOUSE_SENSEITIVITY), glm.vec3(0, 1, 0))
        # roll = glm.quat(0, glm.vec3(0, 0, 1))

        # quat = yaw * pitch * roll

        # viewMatrix = glm.translate(quat,glm.mat4)
        #viewMatrix = quat.toMatrix()
        # glMultMatrixf(viewMatrix)
        #mat = quat.toMatrix()

        #glRotated(degrees(quat.x), 1.0, 0.0, 0.0);
        #glRotated(degrees(quat.y), 0.0, 1.0, 0.0);
        #glRotated(degrees(quat.z), 0.0, 0.0, 1.0);

        #glRotatef(rx * MOUSE_SENSEITIVITY, 1, 0, 0)

        #glRotatef(ry * MOUSE_SENSEITIVITY, 0, 1, 0)

        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * numpy.mat(buffer[:3, :3]) * \
             numpy.mat(buffer[3, :3]).T).reshape(3, 1)
        # c is camera center in absolute coordinates,
        # we need to move it back to (0,0,0)
        # before rotating the camera
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(rx * MOUSE_SENSEITIVITY, m[1], m[5], m[9])
        glRotate(ry * MOUSE_SENSEITIVITY, m[0], m[4], m[8])

        # compensate roll
        glRotated(-math.atan2(-m[4], m[5]) * \
                  57.295779513082320876798154814105, m[2], m[6], m[10])
        #glTranslate(-c[0], -c[1], -c[2])


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

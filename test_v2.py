import sys
import math
import random
import time

import pyglet
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

import pyglet.gl as pgl
from camera import FirstPersonCamera   # mojo

TICKS_PER_SEC = 1

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


def triangle():
    glBegin(GL_LINES)
    # create a line, x,y,z
    glVertex3f(100.0, 100.0, 0.25)
    glVertex3f(200.0, 300.0, -0.75)
    glEnd()

def cube():
    # creating the cubes
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            g = vertices[vertex]
            #v = prim.vertex[vidx]
            #glVertex3fv((GLfloat * 3)(*g))
            pyglet.gl.glVertex3fv((GLfloat * 3)(*g))
    glEnd()
    # coloring
    # glBegin(GL_QUADS)
    # for surface in surfaces:
    #     for vertex in surface:
    #         glColor3fv(colors[0])  # can use other colors in the colors list sticking to red for now
    #         glVertex3fv(vertices[vertex])
    # glEnd()


def main():
    window = pyglet.window.Window(width=800, height=600, caption='Pyglet', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    triangle()
    #camera = FirstPersonCamera(window)
    #camera.update(1)
    #window.set_exclusive_mouse(True)
    pyglet.app.run()
    #main()

if __name__ == '__main__':
    main()

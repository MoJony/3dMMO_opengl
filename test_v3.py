from __future__ import division
import pygame, math, numpy
from OpenGL.GL import *
from OpenGL.GLU import *

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
    (-10,-1,50),
    (10,-1,50),
    (-10,-1,-300),
    (10,-1,-300),

    )

def ground():
    #glEnable(GL_DEPTH_TEST)
    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 0))  # green
        glVertex3fv(vertex)

    glEnd()


def cube():
    # creating the cubes
    # glEnable(GL_DEPTH_TEST)
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

class Player:
    def __init__(self, w=800, h=600, fov=75):
        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | \
                                pygame.DOUBLEBUF)
        glMatrixMode(GL_PROJECTION)
        aspect = w / h
        gluPerspective(fov, aspect, 0.001, 100000.0);
        glMatrixMode(GL_MODELVIEW)
        self.player_x, self.player_y, self.player_z = 0, 0, 0
        # self.player_mat = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
        self.GRAVITY = 0.1
        self.JUMP = 1

    def simple_lights(self):
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.45, 0.0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 10.0, 10.0))
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

    def simple_camera_pose(self):
        """ Pre-position the camera (optional) """
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(numpy.array([0.741, -0.365, 0.563, 0, 0, 0.839, 0.544,
                                   0, -0.671, -0.403, 0.622, 0, -0.649, 1.72, -4.05, 1]))

    # def draw_simple_cube(self):
    #     """ Draw a simple object (optional) """
    #     try:
    #         glEnableClientState(GL_VERTEX_ARRAY);
    #         glVertexPointerf(self.points)
    #         glEnableClientState(GL_NORMAL_ARRAY);
    #         glNormalPointerf(self.normals)
    #         glDrawElementsui(GL_TRIANGLES, self.indices)
    #     except AttributeError:
    #         # a little hack to initialize points only once
    #         self.points = numpy.array([2.4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2.4, 0, 0, \
    #                                    2.4, 0, 2, 0, 0, 2, 0, -1.66, 0, 0, 0, 0, 0, -1.66, 0, 2.4, 0, 0, 0, 0, 0, \
    #                                    2.4, 0, 0, 2.4, -1.66, 2, 2.4, 0, 2, 2.4, -1.66, 2, 0, 0, 2, 2.4, 0, 2, 0, \
    #                                    -1.66, 0, 0, 0, 2, 0, -1.66, 2, 2.4, 0, 0, 0, -1.66, 0, 2.4, -1.66, 0, \
    #                                    2.4, -1.66, 2, 2.4, 0, 0, 2.4, -1.66, 0, 0, 0, 2, 2.4, -1.66, 2, 0, \
    #                                    -1.66, 2, 2.4, -1.66, 2, 0, -1.66, 0, 0, -1.66, 2, 0, -1.66, 0, 2.4,
    #                                    -1.66, 2, 2.4, -1.66, 0], 'f').reshape(-1, 3)
    #
    #         self.normals = numpy.array([0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, \
    #                                     1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 1, 0, 0, 1, \
    #                                     0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, \
    #                                     -1, 0, 0, -1, 0, 0, -1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, \
    #                                     0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0 \
    #                                     ], 'f').reshape(-1, 3)
    #
    #         self.indices = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, \
    #                                     14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, \
    #                                     32, 33, 34, 35], 'i')

    def loop(self):
        pygame.display.flip()
        pygame.event.pump()
        self.keys = dict((chr(i), int(v)) for i, v in \
                         enumerate(pygame.key.get_pressed()) if i < 256)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        return True

    def controls_3d(self, mouse_button=1, w_key='w', s_key='s', space_key = 'space' , a_key='a', \
                    d_key='d'):
        """ The actual camera setting cycle """


        mouse_dx, mouse_dy = pygame.mouse.get_rel()



        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] == 800:
            pygame.mouse.set_pos(1,mouse_pos[1])
        elif mouse_pos[0] == 0:
            pygame.mouse.set_pos((799,mouse_pos[1]))
        elif mouse_pos[1] == 600:
            pygame.mouse.set_pos((1,mouse_pos[1]))
        elif mouse_pos[1] == 0:
            pygame.mouse.set_pos((599,mouse_pos[1]))

        look_speed = .2
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * numpy.mat(buffer[:3, :3]) * \
             numpy.mat(buffer[3, :3]).T).reshape(3, 1)
        # c is camera center in absolute coordinates,
        # we need to move it back to (0,0,0)
        # before rotating the camera
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(mouse_dx * look_speed, m[1], m[5], m[9])
        glRotate(mouse_dy * look_speed, m[0], m[4], m[8])

        # compensate roll
        glRotated(-math.atan2(-m[4], m[5]) * \
                  57.295779513082320876798154814105, m[2], m[6], m[10])
        glTranslate(-c[0], -c[1], -c[2])

        # move forward-back or right-left
        # fwd =   .1 if 'w' is pressed;   -0.1 if 's'
        if (self.player_y > 1):  # mojo is this correct?
            self.player_y = self.player_y - (1 * self.GRAVITY)
        #events = pygame.event.get()
        # for event in events:
        #     pass
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             self.player_y = self.player_y + (1 * self.JUMP)

        fwd = .1 * (self.keys[w_key] - self.keys[s_key])
        strafe = .1 * (self.keys[a_key] - self.keys[d_key])
        if abs(fwd) or abs(strafe):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            # glTra_nslate(fwd * m[2], 0, fwd * m[10])   # "gravity" version? cant aim up and go up
            # glTranslate(strafe * m[0], 0, strafe * m[8])
            # print (m[2])
            glTranslate(fwd * m[2], 0.0, fwd * m[10])  #  ^ "flying" aim up and press forward > go up
            glTranslate(strafe * m[0], strafe * m[4], strafe * m[8])  # mojo - keep this shit

            # for thing in m:
            #     print(thing, end=" / ", flush=True)  # mojo - probs delete
            # print ("new shit \n")

        #self.gravity()

        pygame.mouse.get_rel()

    def gravity(self):
        pass
        #glBegin()
        if (self.player_y > 1):  # mojo is this correct?
            self.player_y = self.player_y - 1
            glTranslate


fps = Player(w=800, h=600, fov=75)
#fps.simple_lights()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
fps.simple_camera_pose()

while fps.loop():
    #fps.draw_simple_cube()
    cube()
    ground()
    glEnable(GL_DEPTH_TEST)
    fps.controls_3d(0, 'w', 's', 'a', 'd')
    if fps.keys['q']: break
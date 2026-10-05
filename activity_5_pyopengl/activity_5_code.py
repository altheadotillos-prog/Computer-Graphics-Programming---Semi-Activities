# Activity 5: Hardware-Accelerated 3D Pipeline using PyOpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
display = (800, 600)

pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption('Activity 5: Hardware Pipeline with PyOpenGL')

# Task 5.1
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -12)

glEnable(GL_DEPTH_TEST)

vertices = [
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
]
colors = [
    (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1), (1,1,1), (0.5,0.5,0.5)
]
surfaces = [
    (0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6)
]

def draw_colored_cube():
    """Task 5.2: Renders a solid 3D cube with distinct colors per vertex."""
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex_idx in surface:
            glColor3fv(colors[vertex_idx])
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def draw_arm_segment():
    """Helper method to draw a simple rectangular limb segment."""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.6, 1.0) 
    for surface in surfaces:
        for vertex_idx in surface:
            x, y, z = vertices[vertex_idx]
            glVertex3f(x * 1.5, y * 0.4, z * 0.4)
    glEnd()

clock = pygame.time.Clock()
rotation_angle = 0.0
arm_base_rot = 0.0
arm_fore_rot = 0.0
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rotation_angle += 1.0
    arm_base_rot += 0.5
    arm_fore_rot = (arm_fore_rot + 1.5) % 360

    # ==========================================
    # OBJECT 1: Standalone Spinning Cube (Task 5.2 & 5.3)
    # ==========================================
    glPushMatrix()
    glTranslatef(-2.5, 0.0, 0.0)
    glRotatef(rotation_angle, 1, 1, 0)
    draw_colored_cube()
    glPopMatrix()

    # ==========================================
    # OBJECT 2: Articulated Arm Hierarchical Modeling (Task 5.3)
    # ==========================================
    glPushMatrix()
    glTranslatef(1.0, 0.0, 0.0)
    
    # -- Base / Shoulder Joint --
    glRotatef(arm_base_rot, 0, 0, 1)
    glTranslatef(1.5, 0.0, 0.0)
    draw_arm_segment()
    
    # -- Forearm / Elbow Joint --
    glTranslatef(1.5, 0.0, 0.0)
    glRotatef(arm_fore_rot, 0, 1, 0)
    glTranslatef(1.5, 0.0, 0.0)
    draw_arm_segment()
    
    glPopMatrix()

    pygame.display.flip()

pygame.quit()

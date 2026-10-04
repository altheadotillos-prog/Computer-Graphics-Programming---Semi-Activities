# ACTIVITY 4: 3D Projection Engine: Orthographic, Oblique (Cavalier/Cabinet), & Perspective
import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Activity 4: 3D Projection Engine: Orthographic, Oblique, & Perspective')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 16, bold=True)
font_title = pygame.font.SysFont('Arial', 22, bold=True)

cube_vertices = [
    [-100, -100, -100], [100, -100, -100], [100, 100, -100], [-100, 100, -100],
    [-100, -100, 100],  [100, -100, 100], [100, 100, 100],  [-100, 100, 100]
]

cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

current_mode = 1  
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0
phi_deg = 30.0
D_val = 400.0

def rotate_x(x, y, z, rad):
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a

def rotate_y(x, y, z, rad):
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a

def rotate_z(x, y, z, rad):
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a, z

def project_orthographic(x, y, z):
    return int(x + 400), int(y + 300)

def project_oblique(x, y, z, mode='cavalier', phi_deg=30):
    phi = math.radians(phi_deg)
    L1 = 1.0 if mode == 'cavalier' else 0.5
    xp = x + z * L1 * math.cos(phi)
    yp = y + z * L1 * math.sin(phi)
    return int(xp + 400), int(yp + 300)

def project_perspective(x, y, z, D=400):
    distance = z + D
    if distance == 0: distance = 0.001
    xp = (x * D) / distance
    yp = (y * D) / distance
    return int(xp + 400), int(yp + 300)

def get_projected_coords(x, y, z, mode):
    if mode == 1:
        return project_orthographic(x, y, z)
    elif mode == 2:
        return project_oblique(x, y, z, mode='cavalier', phi_deg=phi_deg)
    elif mode == 3:
        return project_oblique(x, y, z, mode='cabinet', phi_deg=phi_deg)
    elif mode == 4:
        return project_perspective(x, y, z, D=D_val)
    return 400, 300

running = True
while running:
    clock.tick(60)
    screen.fill((20, 24, 33))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                current_mode = 1
            elif event.key == pygame.K_2:
                current_mode = 2
            elif event.key == pygame.K_3:
                current_mode = 3
            elif event.key == pygame.K_4:
                current_mode = 4
            elif event.key == pygame.K_r:
                angle_x = angle_y = angle_z = 0.0

    keys = pygame.key.get_pressed()
    rot_speed = 0.03
    if keys[pygame.K_x]: angle_x += rot_speed
    if keys[pygame.K_y]: angle_y += rot_speed
    if keys[pygame.K_z]: angle_z += rot_speed

    transformed_vertices = []
    for vert in cube_vertices:
        x, y, z = vert[0], vert[1], vert[2]
        if current_mode == 1 or current_mode == 4:
            x, y, z = rotate_x(x, y, z, angle_x)
            x, y, z = rotate_y(x, y, z, angle_y)
            x, y, z = rotate_z(x, y, z, angle_z)
        transformed_vertices.append((x, y, z))

    projected_points = []
    for vert in transformed_vertices:
        px, py = get_projected_coords(vert[0], vert[1], vert[2], current_mode)
        projected_points.append((px, py))

    if current_mode == 4:
        vanish_x, vanish_y = project_perspective(0, 0, 1000000, D=D_val)
        pygame.draw.circle(screen, (231, 76, 60), (vanish_x, vanish_y), 4)
        for i in range(4, 8):
            px, py = projected_points[i]
            pygame.draw.line(screen, (40, 50, 65), (px, py), (vanish_x, vanish_y), 1)

    for edge in cube_edges:
        p1 = projected_points[edge[0]]
        p2 = projected_points[edge[1]]
        
        is_receding_z_edge = edge in [(0,4), (1,5), (2,6), (3,7)]
        if is_receding_z_edge and current_mode == 4:
            color = (241, 196, 15)  
        else:
            color = (52, 152, 219)  
            
        pygame.draw.line(screen, color, p1, p2, 2)

    mode_names = {
        1: "Orthographic Parallel Projection",
        2: "Oblique Parallel Projection (Cavalier - 100% Depth)",
        3: "Oblique Parallel Projection (Cabinet - 50% Depth)",
        4: "One-Point Perspective Projection Engine"
    }
    
    screen.blit(font_title.render("ACTIVITY 4: 3D Projection Engine", True, (240, 244, 250)), (20, 20))
    screen.blit(font.render(f"Active Framework: {mode_names[current_mode]}", True, (255, 255, 255)), (20, 55))
    
    screen.blit(font.render(f"Rotation Vector Matrix: X={math.degrees(angle_x)%360:.1f}° | Y={math.degrees(angle_y)%360:.1f}° | Z={math.degrees(angle_z)%360:.1f}°", True, (160, 170, 185)), (20, 80))
    
    if current_mode == 4:
        screen.blit(font.render("Vanishing Point convergence mapped at camera anchor core (Red dot)", True, (231, 76, 60)), (20, 105))
    elif current_mode == 2 or current_mode == 3:
        screen.blit(font.render(f"Architectural Scale Rule: Front face matches true scale. Z-Angle={phi_deg}°", True, (46, 204, 113)), (20, 105))

    pygame.display.flip()

pygame.quit()
sys.exit()

# Activity 1: 2D Animation Principles & Kinematics Engine
import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Activity 1: 2D Animation & Kinematics Engine')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 16)

# ---------------------------------------------------------
# GLOBAL ENGINE STATE & DATA CONFIGURATIONS
# ---------------------------------------------------------
current_mode = 1  

# Task 1.1: 
tween_path = [(100, 150), (250, 450), (400, 150), (550, 450), (700, 150), (550, 250), (400, 450), (100, 150)]
current_segment = 0
tween_t = 0.0
tween_speed = 0.015

# Task 1.2: 
poly_start = [(150, 150), (275, 150), (400, 150), (150, 400), (400, 400)]  
poly_end = [(150, 150), (275, 150), (400, 150), (400, 400), (150, 400)]    
morph_t = 0.0
morph_direction = 1

# Task 1.3: 
ball_x, ball_y = 100, 150
ball_vel_y = 0.0
ball_vel_x = 3.5
gravity = 0.4
restitution = 0.82
floor_y = 520
ball_radius = 12

wind_force = 0.08
wind_timer = 0.0

# ---------------------------------------------------------
# INTERPOLATION & CALCULATION ENGINE
# ---------------------------------------------------------
def lerp_point(p1, p2, t):
    """Linear interpolation (LERP) between two 2D coordinate tuples."""
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)

def sine_ease(t):
    """Alternative sinusoidal easing function for smooth edge deceleration."""
    return (1.0 - math.cos(t * math.pi)) / 2.0

def draw_hud():
    """Renders real-time control metrics and structural overlays."""
    modes = {
        1: "Task 1.1: Sinusoidal Constellation Grid Tweening", 
        2: "Task 1.2: 5-Vertex Morph System (Hourglass -> Square)", 
        3: "Task 1.3: Kinematics Engine with Oscillating Wind Drift"
    }
    
    mode_surf = font.render(f"ENGINE_MODE_ACTIVE: {modes[current_mode]}", True, (0, 255, 200))
    ctrl_surf = font.render("TOGGLE_COMMANDS: Press, [2], or [3] to shift engine state", True, (140, 150, 170))
    screen.blit(mode_surf, (25, 20))
    screen.blit(ctrl_surf, (25, 45))
    
    if current_mode == 3:
        reset_surf = font.render("FORCE_RESET: Press [R] to re-inject mass properties", True, (255, 100, 100))
        screen.blit(reset_surf, (25, 70))

# ---------------------------------------------------------
# MAIN ANIMATION RUNTIME EXECUTION LOOP
# ---------------------------------------------------------
running = True
while running:
    clock.tick(60)  
    screen.fill((15, 15, 22))  

    # Task 1.4:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_mode = 1
            elif event.key == pygame.K_2:
                current_mode = 2
            elif event.key == pygame.K_3:
                current_mode = 3
            elif event.key == pygame.K_r and current_mode == 3:
                ball_x, ball_y = 100, 150
                ball_vel_y = 0.0
                ball_vel_x = 3.5
                wind_timer = 0.0

    # --- Task 1.1 ---
    if current_mode == 1:
        if len(tween_path) > 1:
            pygame.draw.lines(screen, (50, 60, 80), False, tween_path, 2)
        for pt in tween_path:
            pygame.draw.circle(screen, (0, 180, 255), pt, 4, 1)

        p_start = tween_path[current_segment]
        p_end = tween_path[current_segment + 1]
        
        eased_time = sine_ease(tween_t)
        sprite_pos = lerp_point(p_start, p_end, eased_time)
        
        pygame.draw.circle(screen, (0, 255, 150), (int(sprite_pos[0]), int(sprite_pos[1])), 10)
        pygame.draw.circle(screen, (255, 255, 255), (int(sprite_pos[0]), int(sprite_pos[1])), 4)
        
        tween_t += tween_speed
        if tween_t >= 1.0:
            tween_t = 0.0
            current_segment += 1
            if current_segment >= len(tween_path) - 1:
                current_segment = 0

    # --- Task 1.2 ---
    elif current_mode == 2:
        morph_t += 0.012 * morph_direction
        if morph_t >= 1.0 or morph_t <= 0.0:
            morph_direction *= -1
            morph_t = max(0.0, min(1.0, morph_t))
            
        rendered_vertices = []
        for idx in range(len(poly_start)):
            v_curr = lerp_point(poly_start[idx], poly_end[idx], morph_t)
            rendered_vertices.append(v_curr)
            
        pygame.draw.polygon(screen, (160, 80, 220), rendered_vertices)
        for vertex in rendered_vertices:
            pygame.draw.circle(screen, (255, 255, 255), (int(vertex[0]), int(vertex[1])), 4)

    # --- Task 1.3 ---
    elif current_mode == 3:
        pygame.draw.line(screen, (180, 40, 70), (0, floor_y), (WIDTH, floor_y), 2)
        
        wind_timer += 0.04
        current_wind = math.sin(wind_timer) * wind_force
        
        ball_vel_x += current_wind
        ball_vel_y += gravity
        
        ball_x += ball_vel_x
        ball_y += ball_vel_y
        
        if ball_x - ball_radius <= 0:
            ball_x = ball_radius
            ball_vel_x *= -1
        elif ball_x + ball_radius >= WIDTH:
            ball_x = WIDTH - ball_radius
            ball_vel_x *= -1
            
        if ball_y + ball_radius >= floor_y:
            ball_y = floor_y - ball_radius
            ball_vel_y = -ball_vel_y * restitution
            
            if abs(ball_vel_y) < 1.0:
                ball_vel_y = 0
                ball_vel_x *= 0.94  

        pygame.draw.circle(screen, (240, 180, 40), (int(ball_x), int(ball_y)), ball_radius)

    draw_hud()
    pygame.display.flip()

pygame.quit()
sys.exit()

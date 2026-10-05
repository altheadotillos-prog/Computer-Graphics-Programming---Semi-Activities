# Activity 3: 3D Coordinate Geometry and Bounding Volumes
import math
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 3: 3D Geometry & Spatial Bounding Volumes")
clock = pygame.time.Clock()

# ==============================================================================
# TASK 3.1: Complete Core Mathematical and Geometry Classes
# ==============================================================================

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def distance_to(self, other: 'Point3D') -> float:
        """Calculates standard 3D Euclidean distance."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    
    def distance_to_sq(self, other: 'Point3D') -> float:
        """Optimization Insight: Bypasses math.sqrt() calculation for performance checks."""
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

    def dot(self, other: 'Point3D') -> float:
        """Calculates the dot product between two vector positions."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Point3D') -> 'Point3D':
        """Calculates the cross product vector between two positions."""
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

class Sphere3D:
    def __init__(self, center: Point3D, radius: float):
        self.center = center
        self.radius = radius

    def contains_point(self, p: Point3D) -> bool:
        """Checks if a point lies within the sphere volume boundaries using squared values."""
        return self.center.distance_to_sq(p) <= (self.radius ** 2)

    def intersects_sphere(self, other: 'Sphere3D') -> bool:
        """OPTIMIZATION INSIGHT: Compare squared distance against squared radius sum."""
        radius_sum = self.radius + other.radius
        return self.center.distance_to_sq(other.center) <= (radius_sum ** 2)

class AABB:
    def __init__(self, min_pt: Point3D, max_pt: Point3D):
        self.min_pt = min_pt
        self.max_pt = max_pt

    def intersects(self, other: 'AABB') -> bool:
        """Evaluates bounding box intersections along all three principal axes."""
        return (self.min_pt.x <= other.max_pt.x and self.max_pt.x >= other.min_pt.x and
                self.min_pt.y <= other.max_pt.y and self.max_pt.y >= other.min_pt.y and
                self.min_pt.z <= other.max_pt.z and self.max_pt.z >= other.min_pt.z)

class SimulatedObject3D:
    def __init__(self, center: Point3D, radius: float):
        self.center = center
        self.radius = radius
        self.sphere = Sphere3D(center, radius)
        self.aabb = AABB(
            Point3D(center.x - radius, center.y - radius, center.z - radius),
            Point3D(center.x + radius, center.y + radius, center.z + radius)
        )
        self.is_colliding_sphere = False
        self.is_colliding_aabb = False

# ==============================================================================
# STUDENT VERIFICATION LOOPS (TASKS 3.2 & 3.3)
# ==============================================================================

def execute_text_verifications():
    print("=" * 70)
    print("                    LABORATORY DATA VERIFICATION METRICS                 ")
    print("=" * 70)
    
    # Task 3.2
    p_32 = Point3D(2, -1, 7)
    q_32 = Point3D(1, -3, 5)
    computed_d = p_32.distance_to(q_32)
    print(f"[Task 3.2] Distance between P(2, -1, 7) and Q(1, -3, 5):")
    print(f"           Calculated d = {computed_d:.3f} | Matches Target (d = 3.0): {math.isclose(computed_d, 3.0)}")
    print("-" * 70)

    # Task 3.3
    coeff_x, coeff_y, coeff_z, offset = 4, -6, 2, 6
    
    h = -coeff_x / 2
    k = -coeff_y / 2
    l = -coeff_z / 2
    
    radius_squared = (h**2 + k**2 + l**2) - offset
    computed_r = math.sqrt(radius_squared)
    
    print(f"[Task 3.3] Input Sphere Polynomial Expression: x^2 + y^2 + z^2 + 4x - 6y + 2z + 6 = 0")
    print(f"           Extracted Center (h, k, l) : ({h}, {k}, {l})")
    print(f"           Extracted Radius (r)       : sqrt({radius_squared}) = {computed_r:.3f}")
    print(f"           Matches Target Center (-2, 3, -1): {h == -2 and k == 3 and l == -1}")
    print(f"           Matches Target Radius sqrt(8)      : {math.isclose(computed_r, math.sqrt(8))}")
    print("=" * 70)

execute_text_verifications()

# ==============================================================================
# TASK 3.4: Broad-Phase Spatial Population & Engine Setup
# ==============================================================================

random.seed(42)
spatial_arena_objects = []

for _ in range(100):
    center_pt = Point3D(
        random.uniform(-140, 140),
        random.uniform(-140, 140),
        random.uniform(180, 450)
    )
    bound_size = random.uniform(8.0, 18.0)
    spatial_arena_objects.append(SimulatedObject3D(center_pt, bound_size))

def process_broad_phase_collisions(object_list):
    """Computes all potential object overlaps via non-sqrt evaluations."""
    for obj in object_list:
        obj.is_colliding_sphere = False
        obj.is_colliding_aabb = False
        
    total_elements = len(object_list)
    for i in range(total_elements):
        for j in range(i + 1, total_elements):
            obj_a = object_list[i]
            obj_b = object_list[j]
            
            if obj_a.sphere.intersects_sphere(obj_b.sphere):
                obj_a.is_colliding_sphere = True
                obj_b.is_colliding_sphere = True
                
            if obj_a.aabb.intersects(obj_b.aabb):
                obj_a.is_colliding_aabb = True
                obj_b.is_colliding_aabb = True

# ==============================================================================
# RENDER PIPELINE CORE (3D-to-2D Perspective Matrix Transformation Engine)
# ==============================================================================

camera_rotation_angle = 0.0

def apply_perspective_projection(point: Point3D, rotation_angle: float):
    """Transforms 3D Cartesian points to 2D Screen coordinates using a basic Camera Matrix."""
    rad_angle = math.radians(rotation_angle)
    centered_x = point.x
    centered_z = point.z - 310
    
    rotated_x = centered_x * math.cos(rad_angle) - centered_z * math.sin(rad_angle)
    rotated_z = centered_x * math.sin(rad_angle) + centered_z * math.cos(rad_angle) + 310
    rotated_y = point.y
    
    if rotated_z < 15:
        rotated_z = 15
        
    focal_lens_scalar = 450
    screen_x = int(WIDTH / 2 + (rotated_x * focal_lens_scalar) / rotated_z)
    screen_y = int(HEIGHT / 2 + (rotated_y * focal_lens_scalar) / rotated_z)
    
    depth_scale = focal_lens_scalar / rotated_z
    return screen_x, screen_y, depth_scale

# ==============================================================================
# MAIN SYSTEM APPLICATION RUNTIME INTERFACE
# ==============================================================================

display_mode = "aabb"
app_running = True

while app_running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
            elif event.key == pygame.K_SPACE:
                display_mode = "sphere" if display_mode == "aabb" else "aabb"
              
    camera_rotation_angle += 0.20

    process_broad_phase_collisions(spatial_arena_objects)

    screen.fill((22, 22, 28))

    spatial_arena_objects.sort(
        key=lambda o: (o.center.x * math.sin(math.radians(camera_rotation_angle)) + 
                       (o.center.z - 310) * math.cos(math.radians(camera_rotation_angle))), 
        reverse=True
    )

    for object_node in spatial_arena_objects:
        sx, sy, scale_factor = apply_perspective_projection(object_node.center, camera_rotation_angle)
        
        if not (-50 <= sx <= WIDTH + 50 and -50 <= sy <= HEIGHT + 50):
            continue
            
        if display_mode == "sphere":
            render_color = (255, 75, 75) if object_node.is_colliding_sphere else (40, 210, 110)
            radius_2d = max(2, int(object_node.radius * scale_factor))
            
            pygame.draw.circle(screen, render_color, (sx, sy), radius_2d, 1)
            pygame.draw.circle(screen, render_color, (sx, sy), 3)
            
        else:
            render_color = (255, 75, 75) if object_node.is_colliding_aabb else (50, 160, 240)
            
            w_2d = int((object_node.aabb.max_pt.x - object_node.aabb.min_pt.x) * scale_factor)
            h_2d = int((object_node.aabb.max_pt.y - object_node.aabb.min_pt.y) * scale_factor)
            
            rect_obj = pygame.Rect(sx - w_2d // 2, sy - h_2d // 2, w_2d, h_2d)
            pygame.draw.rect(screen, render_color, rect_obj, 1)
            pygame.draw.circle(screen, render_color, (sx, sy), 3)

    # ==============================================================================
    # ENGINE DIAGNOSTIC HUD DISPLAY OVERLAYS
    # ==============================================================================
    txt_font = pygame.font.SysFont("Courier New", 16)
    header_font = pygame.font.SysFont("Courier New", 18, bold=True)
    
    hud_bg = pygame.Surface((410, 150))
    hud_bg.set_alpha(215)
    hud_bg.fill((12, 12, 16))
    screen.blit(hud_bg, (15, 15))

    screen.blit(header_font.render("ACTIVITY 3: SPATIAL BOUNDING ENGINE", True, (255, 255, 255)), (25, 25))
    screen.blit(txt_font.render(f"Broad-Phase Evaluation View: {display_mode.upper()}", True, (255, 230, 0)), (25, 55))
    screen.blit(txt_font.render("Press [SPACEBAR] to Toggle Volume Modes", True, (190, 190, 200)), (25, 85))
    screen.blit(txt_font.render(f"Simulation Population Count : {len(spatial_arena_objects)} Entities", True, (190, 190, 200)), (25, 110))
    screen.blit(txt_font.render("Press [ESC] to Exit Simulation Process", True, (140, 140, 145)), (25, 135))

    pygame.display.flip()
pygame.quit()

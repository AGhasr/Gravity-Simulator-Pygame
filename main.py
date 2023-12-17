import pygame
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 720, 450

# Create Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

# Constants for simulation
PLANET_MASS = 100
ROCKET_MASS = 5
FPS = 60
PLANET_RADIUS = 40
ROCKET_RADIUS = 5
VEL_SCALE = 100
PLANET_X = WIDTH // 2
PLANET_Y = HEIGHT // 2
GRAVITY_CONSTANT = 10

# Load images
BACKGROUND = pygame.image.load("space_background.jpg")
ROCKET_IMAGE = pygame.transform.scale(pygame.image.load("rocket.png"), (ROCKET_RADIUS * 5, ROCKET_RADIUS * 5))


class Rocket:
    """
    Class representing a Rocket in the gravity simulation.
    """

    def __init__(self, x, y, vel_x, vel_y, mass, angle):
        """
        Initialize the Rocket with position, velocity, mass, and angle.

        Parameters:
        - x, y: Initial position of the Rocket.
        - vel_x, vel_y: Initial velocity components of the Rocket.
        - mass: Mass of the Rocket.
        - angle: Initial angle of the Rocket.
        """
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.angle = angle

    def move(self):
        """
        Move the Rocket based on gravitational forces and update its position.
        """
        # Calculate gravitational force and update velocity and position
        distance = math.sqrt((self.x - PLANET_X) ** 2 + (self.y - PLANET_Y) ** 2)
        force = (GRAVITY_CONSTANT * self.mass * PLANET_MASS) / distance ** 2

        acceleration = force / self.mass
        angle_to_planet = math.atan2(PLANET_Y - self.y, PLANET_X - self.x)

        acceleration_x = acceleration * math.cos(angle_to_planet)
        acceleration_y = acceleration * math.sin(angle_to_planet)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

        # Update the angle of the Rocket based on its velocity
        self.angle = math.degrees(math.atan2(self.vel_y, self.vel_x))

    def draw(self):
        """
        Draw the Rocket on the Pygame window.
        """
        # Rotate and draw the rocket image based on the Rocket's angle
        rotated_rocket = pygame.transform.rotate(ROCKET_IMAGE, 270 - self.angle)
        rocket_rect = rotated_rocket.get_rect(center=(int(self.x), int(self.y)))
        window.blit(rotated_rocket, rocket_rect.topleft)


def create_rocket(location, mouse_pos):
    """
    Create a Rocket based on the initial location and the mouse position.

    Parameters:
    - location: Initial location of the Rocket.
    - mouse_pos: Current mouse position.

    Returns:
    - Rocket: The created spacecraft.
    """
    # Calculate the angle and velocity components based on the initial location and mouse position
    x1, y1 = location
    x2, y2 = mouse_pos
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    vel_x = (x2 - x1) / 75
    vel_y = (y2 - y1) / 75
    return Rocket(x1, y1, vel_x, vel_y, ROCKET_MASS, angle)


def main():
    """
    Main function for running the gravity simulation.
    """
    running = True
    clock = pygame.time.Clock()

    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(60)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Create a new Rocket when the mouse button is pressed
                if temp_obj_pos:
                    obj = create_rocket(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        window.blit(BACKGROUND, (0, 0))

        for obj in objects:
            # Update and draw each Rocket
            obj.draw()
            obj.move()

            # Remove Rocket that go off-screen or collide with the planet
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - PLANET_X) ** 2 + (obj.y - PLANET_Y) ** 2) <= PLANET_RADIUS
            if off_screen or collided:
                objects.remove(obj)

        if temp_obj_pos:
            # Draw a line and a temporary Rocket when creating a new Rocket
            pygame.draw.line(window, (255, 255, 255), temp_obj_pos, mouse_pos, 2)
            obj = create_rocket(temp_obj_pos, mouse_pos)
            obj.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

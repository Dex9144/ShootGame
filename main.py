import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))  # Create a screen with width 800 and height 600
pygame.display.set_caption("My Simple Game")  # Set the window title

# Define colors (optional)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game loop control
running = True


class Player:
    def __init__(self, x, y, scale, image_path):
        self.original_image = pygame.transform.scale(pygame.image.load(image_path), (scale, scale))
        self.image = self.original_image
        self.pos = pygame.Vector2(x, y)
        self.speed = 3

    def move(self, dx, dy):
        self.pos += pygame.Vector2(dx, dy)

    def draw(self):
        screen.blit(self.image, self.pos)

    def update(self):
        pass


player = Player(100, 100, 100, "png/Player_test.png")


class Weapon:
    def __init__(self, scale, image_path):
        self.original_image = pygame.transform.scale(pygame.image.load(image_path), (scale, scale))
        self.image = self.original_image
        self.pos_offset = pygame.Vector2(0, 8)
        self.pos = pygame.Vector2(0, 0)
        self.angle = 0

        self.point_towards_mouse()

        self.bullets = []

    def point_towards_mouse(self):
        # Get the mouse position and calculate angle to the player center
        mouse_pos = pygame.mouse.get_pos()
        player_center = player.pos + pygame.Vector2(player.image.get_rect().center)
        direction = pygame.Vector2(mouse_pos) - player_center
        angle = +direction.angle_to((1, 0))  # Angle to the horizontal axis
        self.angle = angle

        # Rotate the weapon image to point towards the mouse
        self.image = pygame.transform.rotate(self.original_image, angle)

        # Update the weapon's position so it stays centered on the player
        weapon_rect = self.image.get_rect(center=player_center)
        self.pos = pygame.Vector2(weapon_rect.topleft) + self.pos_offset

    def shoot(self):
        bullet = Bullet(self.pos, 100, self.angle, "png/Bullet.png")
        self.bullets.append(bullet)

    def update(self):
        self.point_towards_mouse()

    def draw(self):
        screen.blit(self.image, self.pos)


shotgun = Weapon(100, "png/Shotgun.png")


class Bullet():
    def __init__(self, vector, scale, angle, image_path):
        self.original_image = pygame.transform.scale(pygame.image.load(image_path), (scale, scale))
        self.image = self.original_image
        self.pos = pygame.Vector2(vector)

        self.angle = shotgun.angle

    def draw(self):
        screen.blit(self.image, self.pos)


shotgun = Weapon(100, "png/Shotgun.png")

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    # Handle movement input
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move(0, -player.speed)  # Move up
    if key[pygame.K_s]:
        player.move(0, player.speed)  # Move down
    if key[pygame.K_a]:
        player.move(-player.speed, 0)  # Move left
    if key[pygame.K_d]:
        player.move(player.speed, 0)  # Move right

    for event in pygame.event.get():
        if event.type == pygame.K_e:
            shotgun.shoot()
    # Drawing
    screen.fill(WHITE)  # Fill the screen with black

    player.draw()  # Draw the player
    shotgun.update()
    shotgun.draw()
    for bullet in shotgun.bullets:
        bullet.draw()
    pygame.display.flip()  # Update the display

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Clean up and quit
pygame.quit()

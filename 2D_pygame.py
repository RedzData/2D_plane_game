import pygame
import pygame.mixer
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Plane Game")

# Load background image
background = pygame.image.load("C:/Users/redzo/2D_game/background.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load player plane image
player_plane_image = pygame.image.load("C:/Users/redzo/2D_game/plane.png").convert_alpha()
player_plane_image = pygame.transform.scale(player_plane_image, (50, 50))
player_plane_rect = player_plane_image.get_rect()

# Load enemy plane image
enemy_plane_image = pygame.image.load("C:/Users/redzo/2D_game/enemy_plane.png").convert_alpha()
enemy_plane_image = pygame.transform.scale(enemy_plane_image, (50, 50))
enemy_plane_rect = enemy_plane_image.get_rect()
enemy_plane_rect.center = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))

# Load laser image
laser_image = pygame.Surface((5, 20))
laser_image.fill((255, 0, 0))  # Red color for the laser

# Load laser sound effect
laser_sound = pygame.mixer.Sound("C:/Users/redzo/2D_game/laser_sound.mp3")  # Replace "laser_sound.wav" with the path to your sound file

# Lists to store lasers and enemy planes
lasers = []
enemy_planes = [enemy_plane_rect]

# Define states
STATE_AVOID = 0
STATE_APPROACH = 1
current_state = STATE_AVOID  # Initial state

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            # Create a laser at the player plane's position
            laser_rect = laser_image.get_rect(center=player_plane_rect.midtop)
            lasers.append(laser_rect)
            
            # Play laser sound effect
            laser_sound.play()
    
    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Update player plane position to follow the mouse and stay within the screen boundaries
    player_plane_rect.centerx = min(max(mouse_x, 0), WIDTH)
    player_plane_rect.centery = min(max(mouse_y, 0), HEIGHT)
    
    # Move lasers
    for laser_rect in lasers:
        laser_rect.y -= 5  # Adjust the speed of the lasers by changing this value
        
        # Remove lasers that have gone off-screen
        if laser_rect.bottom < 0:
            lasers.remove(laser_rect)
    
    # Move enemy planes
    for enemy_plane_rect in enemy_planes:
        if current_state == STATE_AVOID:
            # Calculate the vector from enemy plane to player plane
            direction_x = player_plane_rect.centerx - enemy_plane_rect.centerx
            direction_y = player_plane_rect.centery - enemy_plane_rect.centery
            
            # Normalize the vector
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if length != 0:
                direction_x /= length
                direction_y /= length
            
            # Move enemy plane away from player plane, but not too far
            enemy_plane_rect.move_ip(-direction_x * 3, -direction_y * 3)
            
            # Switch state if enemy plane is far enough from the player
            if length > 150:
                current_state = STATE_APPROACH
        
        elif current_state == STATE_APPROACH:
            # Move enemy plane towards player plane
            dx = mouse_x - enemy_plane_rect.centerx
            dy = mouse_y - enemy_plane_rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                dx /= distance
                dy /= distance
            enemy_plane_rect.move_ip(dx * 2, dy * 2)
            
            # Switch state if enemy plane is close enough to the player
            if distance < 100:
                current_state = STATE_AVOID
    
    # Collision detection
    for laser_rect in lasers:
        for enemy_plane_rect in enemy_planes:
            if laser_rect.colliderect(enemy_plane_rect):
                lasers.remove(laser_rect)
                enemy_planes.remove(enemy_plane_rect)
                # You can add score increment or explosion effect here
    
    # Clear the screen
    screen.blit(background, (0, 0))
    
    # Draw lasers
    for laser_rect in lasers:
        screen.blit(laser_image, laser_rect)
    
    # Draw player plane
    screen.blit(player_plane_image, player_plane_rect)
    
    # Draw enemy planes
    for enemy_plane_rect in enemy_planes:
        screen.blit(enemy_plane_image, enemy_plane_rect)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Lines with Mouse")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Line variables
drawing = False
start_pos = None
lines = []

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                start_pos = event.pos
                drawing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                lines.append((start_pos, end_pos))
                print(f"Line drawn from {start_pos} to {end_pos}")
                drawing = False

    # Draw all the lines
    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 2)

    # Optionally show current preview line
    if drawing and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (150, 150, 150), start_pos, mouse_pos, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()

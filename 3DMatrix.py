import pygame
from pygame.locals import *
import numpy as np
import math

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('3D Rotating Cube')

# Cube vertices (8 points in 3D space)
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

# Define edges of the cube (pairs of vertices)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Rotation matrices
def rotate_x(theta):
    return np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)]
    ])

def rotate_y(theta):
    return np.array([
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ])

def rotate_z(theta):
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])

# Projection matrix (to convert 3D to 2D)
def project(vertex):
    scale = 200  # Zoom factor
    fov = 4  # Field of view factor
    z = vertex[2] + fov  # Depth of the object
    x = vertex[0] * scale / z + width // 2  # X projection
    y = -vertex[1] * scale / z + height // 2  # Y projection
    return int(x), int(y)

# Main loop
running = True
theta_x = 0.01#  # Rotation speed around the X-axis
theta_y = 0.01  # Rotation speed around the Y-axis
theta_z = 0.01  # Rotation speed around the Z-axis

while running:
    x=y=z=0
    keys=pygame.key.get_pressed()
    screen.fill((0, 0, 0))  # Clear screen to black
    if keys[K_w]:
        x=-0.01
    if keys[K_s]:
        x=0.01
    if keys[K_a]:
        y=-0.01
    if keys[K_d]:
        y=0.01
    if keys[K_q]:
        z=-0.01
    if keys[K_e]:
        z=0.01
    # Rotate the cube
    rotation_x = rotate_x(theta_x)
    rotation_y = rotate_y(theta_y)
    rotation_z = rotate_z(theta_z)

    # Apply rotations
    rotated_vertices = np.dot(vertices, rotation_x)  # Rotate around X-axis
    rotated_vertices = np.dot(rotated_vertices, rotation_y)  # Rotate around Y-axis
    rotated_vertices = np.dot(rotated_vertices, rotation_z)  # Rotate around Z-axis

    # Project vertices to 2D
    projected_vertices = [project(vertex) for vertex in rotated_vertices]

    # Draw edges
    for edge in edges:
        start = projected_vertices[edge[0]]
        end = projected_vertices[edge[1]]
        pygame.draw.line(screen, (255, 255, 255), start, end, 2)

    # Update display
    pygame.display.flip()

    # Handle events (to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angles for continuous rotation
    theta_x += x  # Increment rotation around X-axis
    theta_y += y  # Increment rotation around Y-axis
    theta_z += z    # Increment rotation around Z-axis

    # Limit frame rate
    pygame.time.Clock().tick(120)

pygame.quit()

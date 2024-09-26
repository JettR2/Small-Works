# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:40:36 2024

@author: jettr
"""
#%%

import pygame
import numpy as np
import math as m

#%%
# Set up window and clock
Window_size = 700
window = pygame.display.set_mode((Window_size * 7 / 4, Window_size))
clock = pygame.time.Clock()
Rotate_speed = 0.05
scale = 150
angle_x = angle_y = angle_z = 0


projection_matrix = np.matrix([[1,0,0],[0,1,0],[0,0,0]])

# Defining Cube Points
cube_points = [n for n in range(8)]

cube_points[0]=[[-1],[-1],[1]]
cube_points[1]=[[1],[-1],[1]]
cube_points[2]=[[1],[1],[1]]
cube_points[3]=[[-1],[1],[1]]
cube_points[4]=[[-1],[-1],[-1]]
cube_points[5]=[[1],[-1],[-1]]
cube_points[6]=[[1],[1],[-1]]
cube_points[7]=[[-1],[1],[-1]]


def multiply_matrix_method(a, b):
    # Ensure inputs are NumPy arrays
    a = np.array(a)
    b = np.array(b)
    
    # Use NumPy's matmul for fast matrix multiplication
    return np.matmul(a, b)  # Or simply a @ b

def connect_points(i , j , points):
    pygame.draw.line(window, (255,255,255), (points[i][0],points[i][1]) , (points[j][0],points[j][1]) )


# Main Loop
while True:
    
    # Recolor where the points used to be 
    window.fill((0,0,0))
    # Refresh the window 60 times per second
    clock.tick(60)
    
    # Define Rotation Matrices
    Rx = np.array([[1 , 0 , 0 ],
                   [0 , m.cos(angle_x) , -m.sin(angle_x) ],
                   [0 , m.sin(angle_x) , m.cos(angle_x)] ])
     
    Ry = np.array([[ m.cos(angle_y), 0 , m.sin(angle_y)],
                   [ 0 , 1 , 0 ],
                   [-m.sin(angle_y), 0 , m.cos(angle_y)] ])
     
    Rz = np.array([[ m.cos(angle_z), -m.sin(angle_z), 0 ],
                   [ m.sin(angle_z), m.cos(angle_z) , 0 ],
                   [ 0 , 0 , 1 ] ])
    
    # For constant rotation
    # angle_x += 0.03
    # angle_y += 0.03
    # angle_z += 0.03
   
    
    # Point Projection
    points = [0 for _ in range(len(cube_points))]
    i=0
    for point in cube_points:
        
        rotate_x = multiply_matrix_method(Rx,point)
        rotate_y = multiply_matrix_method(Ry,rotate_x)
        rotate_z = multiply_matrix_method(Rz,rotate_y)
        point_2d = multiply_matrix_method(projection_matrix, rotate_z)
        
                
        x = (point_2d[0][0] * scale ) + Window_size * 7/8
        y = (point_2d[1][0] * scale) + Window_size * 0.5
       
        points[i]=(x,y)
        i +=1
        
        
        
        pygame.draw.circle(window,(255,0,0), (x,y),5)
        
    
    connect_points(0, 1, points)
    connect_points(0, 3, points)
    connect_points(0, 4, points)
    connect_points(1, 2, points)
    connect_points(1, 5, points)
    connect_points(2, 6, points)
    connect_points(2, 3, points)
    connect_points(3, 7, points)
    connect_points(4, 5, points)
    connect_points(4, 7, points)
    connect_points(6, 5, points)
    connect_points(6, 7, points)
    
    
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        keys = pygame.key.get_pressed()
        angle_z += Rotate_speed * (keys[pygame.K_e] - keys[pygame.K_q])
        angle_x += Rotate_speed * (keys[pygame.K_w] - keys[pygame.K_s])
        angle_y += Rotate_speed * (keys[pygame.K_d] - keys[pygame.K_a])
        if keys[pygame.K_r]:
            angle_x = angle_y = angle_z = 0

    pygame.display.update()
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 17:01:31 2018

@author: Jens Oppliger
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def distance(pos1, pos2):
    """
    Calculates the distance between two bodies
    """
    return np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1] - pos2[1])**2)


def acceleration(test_body, other_bodies, n):
    """
    Calculates the acceleration of some bodies on a test body
    """
    # Initialize array containing only the positions
    test_body_pos = test_body[n][0:2]
    other_bodies_pos = []
    my_acc_temp = []
    
    for body in other_bodies:
        other_bodies_pos.append(body[n][0:2])
    
    for body_pos in other_bodies_pos:
        r = distance(test_body_pos, body_pos)
        my_acc_temp.append((body_pos - test_body_pos)/r**3)
    
    return sum(my_acc_temp)


def leapfrog(N, t, my_inis):
    """
    Use the leapfrog method to calculate the positions and velocities of the
    individual bodies
    """
    my_bodies = []
    
    # Initialize position&velocity arrays for each body
    for ini in my_inis:
        A = np.zeros(shape=[N, 4])
        A[0] = ini
        my_bodies.append(A)
        
    # Leapfrog method starts here
    for n in range(1, N): # index of the column
        for body in my_bodies:
            i = 0
            body[n][i] = body[n-1][i] + (1/2)*t*body[n-1][i+2] # x coordinate
            body[n][i+1] = body[n-1][i+1] + (1/2)*t*body[n-1][i+3] # y coordinate
            
        # calculate the accelerations
        acc_list = []
        # k := body index for which we calculate the acceleration
        for k in range(0, len(my_bodies)):
            test_body = my_bodies[k]
            other_bodies = [x for i, x in enumerate(my_bodies) if i != k]
            acc_list.append(acceleration(test_body, other_bodies, n))
          
        for body, acc in zip(my_bodies, acc_list):
            i = 0
            body[n][i+2] = body[n-1][i+2] + t*acc[0] # x velocity
            body[n][i+3] = body[n-1][i+3] + t*acc[1] # y velocity
            body[n][i] = body[n][i] + (1/2)*t*body[n][i+2] # update x coordinate
            body[n][i+1] = body[n][i+1] + (1/2)*t*body[n][i+3] # update y coordinate
        
    return my_bodies


if __name__ == '__main__':
    
    N = 1000 # number of calculations
    time_step = 0.02
    
    # Initial conditions and preparing arrays:
    # ========================================================================
    # Zeile ~> Daten zum entsprechenden Massenpunkt m_i pro Durchlauf (# = N)
    # Spalte ~> Einzelne Datenwerte x, y, vx, vy
    ini1 = np.array([0.97000436, -0.24308753, 0.466203685, 0.43236573])
    ini2 = np.array([-0.97000436, 0.24308753, 0.466203685, 0.43236573])
    ini3 = np.array([0, 0, -0.93240737, -0.86473146])
#    ini4 = np.array([0.0, -0.35, -0.3, -0.5])
    
    ini_list = [ini1, ini2, ini3]
#    ini_list = [ini1, ini2, ini3, ini4]
    # ========================================================================
    
    my_data = leapfrog(N, time_step, ini_list)
    
    m1, m2, m3 = my_data[0], my_data[1], my_data[2]
#    m1, m2, m3, m4 = my_data[0], my_data[1], my_data[2], my_data[3]
    
    # Plot / Animation (für 3 Körper)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, facecolor='black')
    line_anim1, = ax.plot([], [] , 'ro', markersize=10)
    line_anim2, = ax.plot([], [] , 'bo', markersize=10)
    line_anim3, = ax.plot([], [] , 'go', markersize=10)
#    line_anim4, = ax.plot([], [] , 'o', color='white', markersize=10)

    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-0.6, 0.6])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.plot(m1[:,0], m1[:,1], '--', color='white')
    ax.plot(m2[:,0], m2[:,1], '--', color='white')
    ax.plot(m3[:,0], m3[:,1], '--', color='white')
#    ax.plot(m4[:,0], m4[:,1], '--', color='white')

    def init():
        line_anim1.set_data([], [])
        line_anim2.set_data([], [])
        line_anim3.set_data([], [])
#        line_anim4.set_data([], [])
        return line_anim1, line_anim2, line_anim3,
#        return line_anim1, line_anim2, line_anim3, line_anim4
    
    def animate(i):
        line_anim1.set_data(m1[:,0][i], m1[:,1][i])
        line_anim2.set_data(m2[:,0][i], m2[:,1][i])
        line_anim3.set_data(m3[:,0][i], m3[:,1][i])
#        line_anim4.set_data(m4[:,0][i], m4[:,1][i])
        return line_anim1, line_anim2, line_anim3,
#        return line_anim1, line_anim2, line_anim3, line_anim4
    
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=2000, interval=20, blit=True)
       

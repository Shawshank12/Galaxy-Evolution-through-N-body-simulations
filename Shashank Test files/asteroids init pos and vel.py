# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 20:58:58 2022

@author: Shashank
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('D:\KSP 3.0\Galaxy-Evolution-through-N-body-simulations\Solar_System_using_Barnes_Hut')
import barnes_hut as bh
import time

begin = time.time()

def c2p(arr):
    radius = np.sqrt(arr[0]**2 + arr[1]**2)
    angle = np.arctan2(arr[1], arr[0])
    return radius, angle

n = 200
r = []
theta = []
asteroids = []
sun = bh.cel_obj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.989e30)
for i in range(n):
    if i == 0:
        asteroids.append(sun)
    b = 229e9 + np.random.random()*(777e9 - 229e9)
    r.append(b)
    c = 2*np.pi*np.random.random()
    v_b = 5e2 + np.random.random()*(30e3 - 1e2)
    theta.append(c)
    mass = 1e2 + np.random.random()*2e5
    obj = bh.cel_obj(b*np.cos(c), b*np.sin(c), 0, -1*v_b*np.sin(c), v_b*np.cos(c), 0, mass)
    asteroids.append(obj)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(theta, r)
ax.set_rmax(1e12)
ax.set_rlabel_position(-22.5)
ax.grid(True)

t_0 = 0
t = t_0
dt = 86400
t_end = 86400 * 365 * 1
t_array = np.arange(t_0, t_end, dt)
BIG_G = 6.67e-11

positions = np.array([x.pos for x in asteroids])
velocities = np.array([x.vel for x in asteroids])
masses = np.array([x.m for x in asteroids])

fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
ax2.set_rmax(1e12)
ax2.set_rlabel_position(-22.5)
ax2.grid(True)
ke = []
pe = []
e = []
e_scale = 1e15
while t<t_end:
    en = 0
    p = 0
    a_g = bh.GravAccel(positions, masses)
    for m1_id in range(len(asteroids)):                 
        asteroids[m1_id].vel += a_g[m1_id] * dt
        velocities[m1_id] = asteroids[m1_id].vel
    for e_id in range(len(asteroids)):
        asteroids[e_id].pos += asteroids[e_id].vel * dt
        positions[e_id] = asteroids[e_id].pos
    for i in range(len(asteroids)):
        en += 0.5 * asteroids[i].m * np.linalg.norm(asteroids[i].vel)**2
    for i in range(len(asteroids)):
        for j in range(i+1, len(asteroids)):
            if i != j:
                dist = np.linalg.norm(asteroids[i].pos - asteroids[j].pos) + 0.0001
                p += (-1 * BIG_G * asteroids[i].m * asteroids[j].m)/dist
    ke.append(en/e_scale)
    pe.append(p/e_scale)
    e.append((en+p)/e_scale)
    r_p = []
    theta_p = []
    for i in range(len(asteroids)):
        ra, th = c2p(asteroids[i].pos)
        r_p.append(ra)
        theta_p.append(th)
    ax2.scatter(theta_p, r_p)
    fig2.savefig('D:\KSP 3.0\Plots\plot_{}.png'.format(t/86400), dpi=600)
    ax2.cla()
    t += dt

fig3 = plt.figure()
plt.plot(t_array, ke)
fig3 = plt.figure()
plt.plot(t_array, pe)
fig5 = plt.figure()
plt.plot(t_array, e)

end = time.time()
print(end - begin)
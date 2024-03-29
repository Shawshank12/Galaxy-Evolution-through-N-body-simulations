# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 00:06:43 2022

@author: Shashank
"""
import sys
sys.path.append('D:\KSP 3.0\Galaxy-Evolution-through-N-body-simulations\Solar_System_using_Barnes_Hut')
import matplotlib.pyplot as plt
import numpy as np
import plummer_model_alt as plum
from mpl_toolkits import mplot3d
import barnes_hut
import time
from matplotlib.animation import FuncAnimation

begin = time.time() 

scale = 1e10

sc = plum.make_plummer(1000, 1e20, scale)
print(sc.energy_vals())

positions = np.array([x.pos for x in sc.body])
velocities = np.array([x.vel for x in sc.body])
masses = np.array([x.mass for x in sc.body])

com = sum([positions[i]*masses[i] for i in range(len(positions))])/1e20
print(com)

t_0 = 0
t = t_0
n_years = 100
dt = 86400*365
t_end = 86400 * 365 * n_years
t_array = np.arange(t_0, t_end, dt)

fig = plt.figure(dpi=600)
ax = plt.axes(projection='3d')
plot_scale = 5e10
ax.set_xlim(left=com[0] - plot_scale, right=com[0] + plot_scale) 
ax.set_ylim(bottom=com[1] - plot_scale, top=com[1] + plot_scale) 
ax.set_zlim(bottom=com[2] - plot_scale, top=com[2] + plot_scale)
plt.autoscale(False)

x_i = [obj[0] for obj in positions]
y_i = [obj[1] for obj in positions]
z_i = [obj[2] for obj in positions]
ax.scatter(x_i, y_i, z_i, s=0.5)
 
j = 1

ke = []
pe = []
e = []

x_tot = []
y_tot = []
z_tot = []
while t<t_end:
    a_g = barnes_hut.GravAccel(positions, masses)
    for m1_id in range(len(sc.body)):                 
        sc.body[m1_id].vel += a_g[m1_id] * dt
        velocities[m1_id] = sc.body[m1_id].vel
    for e_id in range(len(sc.body)):
        sc.body[e_id].pos += sc.body[e_id].vel * dt
        positions[e_id] = sc.body[e_id].pos
    k, p, tot = sc.energy_vals()
    ke.append(k)
    pe.append(p)
    e.append(tot)
    
    x = []
    y = []
    z = []
    for i in sc.body:
        x.append(i.pos[0])
        y.append(i.pos[1])
        z.append(i.pos[2])
    x_tot.append(x)  
    y_tot.append(y) 
    z_tot.append(z) 
    print("Step {} done".format(j))
    j += 1
    t += dt

def update_func(i):
    ax.cla()
    plot_scale = 5e10
    ax.set_xlim(left=com[0] - plot_scale, right=com[0] + plot_scale) 
    ax.set_ylim(bottom=com[1] - plot_scale, top=com[1] + plot_scale) 
    ax.set_zlim(bottom=com[2] - plot_scale, top=com[2] + plot_scale)
    ax.scatter(x_tot[i], y_tot[i], z_tot[i], s=0.6)   
    print("frame {} rendered".format(i))
animation = FuncAnimation(fig, update_func, interval = 17, save_count=n_years)
animation.save("cluster.gif", dpi=600)

fig2 = plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.plot(t_array, ke)
plt.plot(t_array, pe)
plt.plot(t_array, e)
fig3 = plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Kinetic Energy (J)")
plt.plot(t_array, ke)
fig4 = plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Potential Energy (J)")
plt.plot(t_array, pe)
fig5 = plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Total Energy (J)")
plt.plot(t_array, e)

end = time.time()
print(end - begin)
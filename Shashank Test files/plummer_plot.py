import matplotlib.pyplot as plt
import numpy as np
import plummer_model_alt as plum
from mpl_toolkits import mplot3d

sc = plum.make_plummer(1000, 1e20, 1e10)
print(sc.energy_vals())

positions = np.array([x.pos for x in sc.body])
velocities = np.array([x.vel for x in sc.body])
masses = np.array([x.mass for x in sc.body])

x = [obj[0] for obj in positions]
y = [obj[1] for obj in positions]
z = [obj[2] for obj in positions]

radii = [np.linalg.norm(positions[i]) for i in range(len(positions))]
speeds = [np.linalg.norm(velocities[i]) for i in range(len(velocities))]
counts1, bins1 = np.histogram(radii, bins=20)
plt.xlabel("radius (m)")
plt.ylabel("counts")
plt.stairs(counts1, bins1)
f = plt.figure()
counts2, bins2 = np.histogram(speeds, bins=20)
plt.xlabel("speed (m/s)")
plt.ylabel("counts")
plt.stairs(counts2, bins2)
    
fig = plt.figure(dpi=600)
ax = plt.axes(projection='3d')
a = 5e10
ax.axes.set_xlim3d(left=-1*a, right=a) 
ax.axes.set_ylim3d(bottom=-1*a, top=a) 
ax.axes.set_zlim3d(bottom=-1*a, top=a)
ax.scatter3D(x,y,z, s=0.5)


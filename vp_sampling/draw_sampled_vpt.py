import math, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

ele_max = 60
#til_max = 10 #+-til_max
sample = 100000


#################### generate label ####################
ele = [7.5,22.5,37.5,52.5]  # 0~20

azi = [
       [0.00, 15.00,30.00,45.00,60.00,75.00,
        90.00,105.00,120.00,135.00,150.00,165.00,
        180.00,195.00,210.00,225.00,240.00,255.00,
        270.00,285.00,300.00,315.00,330.00,345.00],

       [0.00,17.14,34.29,51.43,68.57,85.71,102.86,
        120.00,137.14,154.29,171.43,188.57,205.71,222.86,
        240.00,257.14,274.29,291.43,308.57,325.71,342.86],
       
       [0.00,21.18,42.35,63.53,84.71,105.88,127.06,148.24,169.41,
        190.59,211.76,232.94,254.12,275.29,296.47,317.65,338.82],

       [0.00,30.00,60.00,90.00,120.00,150.00,180.00,210.00,240.00,270.00,300.00,330.00]]

X_label = []
Y_label = []
Z_label = []
A_label = []
E_label = []
L_num = []
L_names = []
n = 0

for i, e in enumerate(ele):
	for a in azi[i]:
		E_label.append(e)
		A_label.append(a)
		X_label.append(math.cos(a*math.pi/180)*math.cos(e*math.pi/180))
		Y_label.append(math.sin(a*math.pi/180)*math.cos(e*math.pi/180))
		Z_label.append(math.sin(e*math.pi/180))
		L_num.append(n)
		n += 1
		L_names.append(['azi=%s_ele=%s'%(a, e)])    


print('label numbers: %d'%len(X_label))
np.savetxt('label.names', L_names, fmt='%s')

colormap = []
for i in range(len(X_label)):
    colormap.append([np.random.random(),np.random.random(),np.random.random()])
#################### generate label ####################

X = []
Y = []
Z = []
A = []
E = []
T = []
D = []
L = []
C = []

increment = math.pi * (3. - math.sqrt(5.))
sample *= 4
offset = 2./sample
for i in range(sample):
    z = ((i * offset) - 1) + (offset / 2)
    if z >= 0 and z < math.sin((ele_max)*math.pi/180):
        ele = math.asin(z)
        phi = ((i + 1) % sample) * increment

        A.append((phi*180/math.pi) % 360)
        E.append(ele*180/math.pi)  # E.append(10)
        T.append(0.)  # T.append((np.random.rand()-0.5)*2*til_max)
        D.append(1.5)  # D.append(np.random.rand()*9+1)
        L.append(0)
        
        r = math.sqrt(1 - pow(z,2))
        y = math.sin(phi) * r
        x = math.cos(phi) * r
        X.append(x)
        Y.append(y)
        Z.append(z)
        d = []
        for j in range(len(X_label)):
            dis = math.sqrt( (x-X_label[j])**2 + (y-Y_label[j])**2 + (z-Z_label[j])**2 )
            d.append(dis)
        la = d.index(min(d))
        #L.append(la)
        C.append(colormap[la])
        

a = [A,E,T,D,L]
b = np.swapaxes(a,1,0)

view_parameter = np.swapaxes([A, E, T, D, L], 1, 0)

save_dir = '../data/view_distribution'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
np.savetxt(save_dir + '/car.txt',
           view_parameter,
           fmt='%.3f %.3f %.3f %.3f %d')

f1 = plt.figure(1)
ax = Axes3D(f1)
ax.scatter(X_label, Y_label, Z_label, s=10, c=colormap )
ax.auto_scale_xyz([-1,1],[-1,1],[0,1])

f2 = plt.figure(2)
ax = Axes3D(f2)
ax.scatter(X, Y, Z, s=0.1, c=C )
ax.auto_scale_xyz([-1,1],[-1,1],[0,1])
plt.show()


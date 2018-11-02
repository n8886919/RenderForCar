import math, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

ele_max = 60 #30
#til_max = 10 #+-til_max
sample = 1000000

'''
#################### generate label ####################
azi = range(0,360,15) # 0~360
print(azi)
#azi = [0,45,90,135,180,225,270,315]
#ele = [5,15,25]  # 0~20
#til = [-10,-5,0,5,10]  # +-10
X_label = []
Y_label = []
Z_label = []
A_label = []
E_label = []
L_num = []
L_names = []
n = 0
for a in azi:
	for e in ele:
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
'''  
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

		A.append((phi*180/math.pi)%360)
		E.append(ele*180/math.pi) #E.append(10)
		T.append(0.) #T.append((np.random.rand()-0.5)*2*til_max)
		D.append(1.5) #D.append(np.random.rand()*9+1)
		L.append(0)
		'''		
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
		L.append(la)
		C.append(colormap[la])
		'''
'''
a = [A,E,T,D,L]
b = np.swapaxes(a,1,0)
np.savetxt('data/view_distribution/car24_no_tile.txt', b, fmt='%.3f %.3f %.3f %.3f %d')
'''
view_parameter = np.swapaxes([A,E,T,D,L],1,0)
np.savetxt('data/view_distribution/no_label_elemax60.txt', view_parameter, 
	fmt='%.3f %.3f %.3f %.3f %d')
'''
f1 = plt.figure(1)
ax = Axes3D(f1)
ax.scatter(X_label, Y_label, Z_label, s=10, c=colormap )
ax.auto_scale_xyz([-1,1],[-1,1],[0,1])  
      
f2 = plt.figure(2)
ax = Axes3D(f2)
ax.scatter(X, Y, Z, s=0.1, c=C )
ax.auto_scale_xyz([-1,1],[-1,1],[0,1])
plt.show()
'''
